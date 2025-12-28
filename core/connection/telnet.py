# core/connection/telnet.py

import asyncio
import telnetlib3
from config.secrets import TELNET_USERNAME, TELNET_PASSWORD, TELNET_PORT

async def connect(host: str):
    reader, writer = await telnetlib3.open_connection(
        host=host,
        port=TELNET_PORT,
        connect_minwait=0.5,
        connect_maxwait=3.0,
    )

    writer.write(TELNET_USERNAME + "\n")
    await asyncio.sleep(0.2)

    writer.write(TELNET_PASSWORD + "\n")
    await asyncio.sleep(0.5)

    return reader, writer


async def send_bulk(reader, writer, commands, timeout=2.0) -> str:
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