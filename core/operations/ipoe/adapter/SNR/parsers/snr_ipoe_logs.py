import asyncio
import re

from core.operations.ipoe.adapter.SNR.commands import (
    SHOW_LOGGING_FLASH,
    SHOW_LOGGING_INCLUDE,
)


async def snr_collect_logs_fast(
    reader,
    writer,
    port: str,
    limit: int = 15,
) -> list[str]:
    logs: list[str] = []
    port_re = re.escape(port)

    pattern = re.compile(
        rf"(\d+)\s+(%[A-Za-z]+\s+\d+\s+\d+:\d+:\d+).*?"
        rf"Ethernet{port_re}.*?(UP|DOWN)",
        re.I,
    )

    writer.write(SHOW_LOGGING_FLASH + "\n")

    buffer = ""
    while True:
        chunk = await reader.read(2048)
        if not chunk:
            break

        buffer += chunk

        for line in buffer.splitlines():
            m = pattern.search(line)
            if m:
                logs.append(
                    f"{m.group(1)} {m.group(2)} - {m.group(3).upper()}"
                )
                if len(logs) >= limit:
                    return logs

        if "--More--" in chunk or "more" in chunk.lower():
            writer.write(" ")
            await asyncio.sleep(0.05)

        buffer = buffer[-2048:]

    return logs


async def snr_collect_logs_include(
    reader,
    writer,
    port: str,
    limit: int = 15,
) -> list[str]:
    logs: list[str] = []
    port_num = port.split("/")[-1]

    iface_re = re.compile(rf"\bEthernet1/0/{port_num}\b", re.I)
    pattern = re.compile(
        r"(\d+)\s+(%[A-Za-z]+\s+\d+\s+\d+:\d+:\d+).*?(UP|DOWN)",
        re.I,
    )

    writer.write(
        SHOW_LOGGING_INCLUDE.format(port_num=port_num) + "\n"
    )

    raw = ""
    while True:
        chunk = await reader.read(2048)
        if not chunk:
            break
        raw += chunk

    for line in raw.splitlines():
        if not iface_re.search(line):
            continue

        m = pattern.search(line)
        if m:
            logs.append(
                f"{m.group(1)} {m.group(2)} - {m.group(3).upper()}"
            )
            if len(logs) >= limit:
                break

    return logs
