import re, asyncio
from ..constants import clean_line
from ..commands import SHOW_LOG, ENABLE_CLIPAGING

async def get_device_logs(reader, writer, port: int, max_logs: int = 15):
    writer.write(f"{SHOW_LOG}\n")
    await writer.drain()
    await asyncio.sleep(0.3)

    logs = []
    port_regex = re.compile(
        rf"\b(port\s+{port}|Port\s+{port}|Port Number\s*:\s*{port})\b",
        re.IGNORECASE,
    )

    pager_tokens = ("Next Page", "SPACE", "CTRL+C", "Quit", "ESC")
    prompt_re = re.compile(r".+#$")

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=2.0)
            if not chunk:
                break

            for raw in chunk.splitlines():
                line = clean_line(raw)
                if not line:
                    continue

                if prompt_re.match(line):
                    return logs[-max_logs:]

                if any(tok in line for tok in pager_tokens):
                    continue

                if port_regex.search(line):
                    logs.append(line)
                    if len(logs) >= max_logs:
                        writer.write("q")
                        await writer.drain()
                        return logs[-max_logs:]

            if any(tok in chunk for tok in pager_tokens):
                writer.write(" ")
                await writer.drain()
                await asyncio.sleep(0.3)

        except asyncio.TimeoutError:
            break

    # Включаем clipaging обратно после завершения
    writer.write(f"{ENABLE_CLIPAGING}\n")
    await writer.drain()

    return logs[-max_logs:]
