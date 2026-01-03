# core/connection/telnet.py

import asyncio
import re
import telnetlib3
import socket

from config.secrets import TELNET_USERNAME, TELNET_PASSWORD, TELNET_PORT


# =========================
# PROMPTS
# =========================

DEFAULT_PROMPT_RE = re.compile(r"\)#|\(cfg\)#|>$")
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
                connect_minwait=0.5,
                connect_maxwait=3.0,
            ),
            timeout=5,
        )

        writer.write(TELNET_USERNAME + "\n")
        await asyncio.sleep(0.2)

        writer.write(TELNET_PASSWORD + "\n")
        await asyncio.sleep(0.5)

        return reader, writer

    except asyncio.TimeoutError:
        raise TelnetConnectionError(
            f"Connection timeout to host {host}"
        )
    except socket.gaierror:
        raise TelnetConnectionError(
            f"Host {host} does not exist or DNS resolution failed"
        )
    except ConnectionRefusedError:
        raise TelnetConnectionError(
            f"Connection refused by host {host}"
        )
    except OSError as e:
        raise TelnetConnectionError(
            f"Network error while connecting to {host}: {e}"
        )


# =========================
# LOW LEVEL READ
# =========================

async def read_until_prompt(
    reader,
    writer,
    prompt_re,
    timeout: float = 0.5,
    handle_paging: bool = False,
) -> str:
    output = ""

    try:
        while True:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
            if not chunk:
                break

            output += chunk

            if handle_paging and ("--More--" in chunk or "more" in chunk.lower()):
                writer.write(" ")
                await asyncio.sleep(0.05)
                continue

            if prompt_re.search(chunk):
                break

    except asyncio.TimeoutError:
        pass

    return output


# =========================
# GPON / LEGACY BULK
# =========================

async def send_bulk(reader, writer, commands, timeout: float = 2.0) -> str:
    marker = "===END==="
    payload = "\n".join(commands + [f"echo {marker}"]) + "\n"

    writer.write(payload)
    output = ""

    try:
        while True:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
            if not chunk:
                break

            output += chunk

            if marker in chunk:
                break

    except asyncio.TimeoutError:
        pass

    return output


# =========================
# IPOE (PROMPT-BASED)
# =========================

async def send_ipoe(
    reader,
    writer,
    commands,
    *,
    prompt_re=DEFAULT_PROMPT_RE,
    handle_paging: bool = False,
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

    return output
