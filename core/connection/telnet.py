import asyncio
import telnetlib3
from config.secrets import TELNET_USERNAME, TELNET_PASSWORD, TELNET_PORT

async def connect(host: str):
    reader, writer = await telnetlib3.open_connection(
        host=host,
        port=TELNET_PORT,
        connect_minwait=0.2,
        connect_maxwait=1
    )
    writer.write(TELNET_USERNAME + "\n")
    await asyncio.sleep(0.3)
    writer.write(TELNET_PASSWORD + "\n")
    await asyncio.sleep(0.5)
    return reader, writer

async def send(reader, writer, command: str, timeout=0.3) -> str:
    writer.write(command + "\n")
    output = ""

    try:
        while True:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
            if not chunk:
                break
            output += chunk
    except asyncio.TimeoutError:
        pass

    return output
