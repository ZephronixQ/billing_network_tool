import asyncio

async def send_command(reader, writer, command):
    writer.write(command + '\n')
    output = ''

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=0.2)
            output += chunk
            if '----- more -----' in chunk:
                writer.write('\n')

        except asyncio.TimeoutError:
            break

    return output