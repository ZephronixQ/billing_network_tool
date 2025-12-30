import asyncio

async def send_command(reader, writer, command: str, timeout=1.5) -> str:
    writer.write(command + "\n")
    await writer.drain()
    await asyncio.sleep(0.3)

    output = ""

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
            if not chunk:
                break
            output += chunk
        except asyncio.TimeoutError:
            break

    return output
