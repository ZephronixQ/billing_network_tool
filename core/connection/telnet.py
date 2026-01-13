import asyncio
import re
import telnetlib3
import socket
import time

from config.secrets import TELNET_USERNAME, TELNET_PASSWORD, TELNET_PORT

# =========================
# PROMPTS
# =========================

DEFAULT_PROMPT_RE = re.compile(r"\)#|\(cfg\)#|>\s*$")
SNR_PROMPT_RE = re.compile(r"#\s*$")

class TelnetConnectionError(Exception):
    pass

# =========================
# CONNECTION
# =========================

async def connect(host: str):
    try:
        reader, writer = await asyncio.wait_for(
            telnetlib3.open_connection(
                host=host,
                port=TELNET_PORT,
                connect_minwait=0.2,
                connect_maxwait=1.5,
            ),
            timeout=3,
        )

        writer.write(TELNET_USERNAME + "\n")
        await asyncio.sleep(0.1)

        writer.write(TELNET_PASSWORD + "\n")
        await asyncio.sleep(0.2)

        return reader, writer

    except asyncio.TimeoutError:
        raise TelnetConnectionError(f"Connection timeout to host {host}")
    except socket.gaierror:
        raise TelnetConnectionError(f"Host {host} does not exist or DNS failed")
    except ConnectionRefusedError:
        raise TelnetConnectionError(f"Connection refused by host {host}")
    except OSError as e:
        raise TelnetConnectionError(f"Network error while connecting to {host}: {e}")

# =========================
# LOW LEVEL READ (FIXED)
# =========================

async def read_until_prompt(
    reader,
    writer,
    *,
    prompt_re,
    timeout: float = 1.5,
    handle_paging: bool = False,
    chunk_size: int = 4096,
) -> str:
    buf = ""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        try:
            chunk = await asyncio.wait_for(
                reader.read(chunk_size),
                timeout=0.3,
            )
        except asyncio.TimeoutError:
            break

        if not chunk:
            break

        buf += chunk

        # ===== pager =====
        if handle_paging and ("--More--" in chunk or "more" in chunk.lower()):
            writer.write(" ")
            continue

        # ===== prompt =====
        if prompt_re.search(buf):
            break

    return buf

# =========================
# GPON / LEGACY BULK
# =========================

async def send_bulk(reader, writer, commands, timeout: float = 2.0) -> str:
    marker = "===END==="
    payload = "\n".join(commands + [f"echo {marker}"]) + "\n"

    writer.write(payload)
    buf = ""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=0.5)
        except asyncio.TimeoutError:
            break

        if not chunk:
            break

        buf += chunk
        if marker in buf:
            break

    return buf

# =========================
# IPOE (PROMPT-BASED)
# =========================

async def send_ipoe(
    reader,
    writer,
    commands,
    *,
    prompt_re=DEFAULT_PROMPT_RE,
    handle_paging: bool = True,
) -> str:
    output = ""

    for cmd in commands:
        writer.write(cmd + "\n")
        await writer.drain()

        chunk = await read_until_prompt(
            reader,
            writer,
            prompt_re=prompt_re,
            handle_paging=handle_paging,
        )
        output += chunk

        while True:
            try:
                tail = await asyncio.wait_for(reader.read(1024), timeout=0.05)
                if not tail:
                    break
                output += tail.decode(errors="ignore") if isinstance(tail, bytes) else tail
            except asyncio.TimeoutError:
                break

    return output

ELTEX_PROMPT_RE = re.compile(r"\n?\S+#\s*$")

async def send_ipoe_eltex(
    reader,
    writer,
    commands,
    *,
    timeout: float = 3.0,
) -> str:
    output = ""

    for cmd in commands:
        writer.write(cmd + "\n")
        await writer.drain()

        buf = ""

        while True:
            try:
                chunk = await asyncio.wait_for(
                    reader.read(4096),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                break

            if not chunk:
                break

            chunk = chunk.replace("\r", "")
            buf += chunk

            # ===== paging =====
            if "---- More ----" in chunk or "More:" in chunk:
                writer.write(" ")
                await writer.drain()
                continue

            # ===== prompt =====
            if ELTEX_PROMPT_RE.search(buf):
                break

        output += buf

    return output

# =========================
# D-LINK 
# =========================
# ---------- REGEX ----------

ANSI_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
PROMPT_RE = re.compile(r"[>#]\s*$")
PAGER_RE = re.compile(r'CTRL\+C.*Quit', re.IGNORECASE)

# ---------- CLEAN ----------
def clean(line: str) -> str:
    line = ANSI_RE.sub('', line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)
    return line.strip()

# ---------- READ ----------
async def read_until_prompt_dlink(
    reader,
    writer=None,
    *,
    timeout: float = 3.0,
    quiet: float = 1.5,
) -> list[str]:

    lines: list[str] = []
    loop = asyncio.get_event_loop()
    last_data = loop.time()

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
        except asyncio.TimeoutError:
            if loop.time() - last_data >= quiet:
                break
            continue

        if not chunk:
            break

        last_data = loop.time()

        for raw in chunk.splitlines():
            cl = clean(raw)
            if cl:
                lines.append(cl)

        if PROMPT_RE.search(chunk):
            break

    return lines

# ---------- SEND ----------
async def send_ipoe_dlink(
    reader,
    writer,
    commands: list[str],
) -> list[str]:

    output: list[str] = []

    for cmd in commands:
        writer.write(cmd + "\n")
        await writer.drain()

        lines = await read_until_prompt_dlink(
            reader,
            writer,
            timeout=3.0,
            quiet=1.5,
        )
        output.extend(lines)

    return output
