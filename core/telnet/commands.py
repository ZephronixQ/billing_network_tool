import asyncio
import telnetlib3


async def send_command_fast(
    reader: telnetlib3.TelnetReader,
    writer: telnetlib3.TelnetWriter,
    command: str
) -> str:

    writer.write(command + "\n")
    output = ""

    try:
        while True:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=0.25)
            if not chunk:
                break
            output += chunk
    except asyncio.TimeoutError:
        pass

    return output