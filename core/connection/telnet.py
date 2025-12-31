# core/connection/telnet.py

import asyncio
import re
import telnetlib3

from config.secrets import TELNET_USERNAME, TELNET_PASSWORD, TELNET_PORT


PROMPT_RE = re.compile(r'\)#|\(cfg\)#|>$')

class TelnetConnectionError(Exception):
    pass

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

        # ===== LOGIN =====
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
# GPON / legacy bulk sender
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
# IPOE sender (prompt-based)
# =========================
async def send_ipoe(reader, writer, commands, timeout: float = 0.5) -> str:
    output = ""

    for cmd in commands:
        writer.write(cmd + "\n")
        await writer.drain()

        try:
            while True:
                chunk = await asyncio.wait_for(reader.read(4096), timeout)
                if not chunk:
                    break

                output += chunk

                if PROMPT_RE.search(chunk):
                    break

        except asyncio.TimeoutError:
            pass

    return output

