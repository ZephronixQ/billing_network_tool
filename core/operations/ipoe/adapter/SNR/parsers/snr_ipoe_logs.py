# core/operations/ipoe/adapter/SNR/logs.py

import re

from core.connection.telnet import read_until_prompt, SNR_PROMPT_RE
from core.operations.ipoe.adapter.SNR.commands import (
    SHOW_LOGGING_FLASH,
    SHOW_LOGGING_INCLUDE,
)


async def snr_collect_logs(
    reader,
    writer,
    port: str,
    model: str,
    limit: int = 10,
) -> list[str]:
    iface = f"Ethernet{port}"
    logs: list[str] = []

    # ==========================
    # enable paging
    # ==========================
    writer.write("terminal length 24\n")
    await read_until_prompt(
        reader,
        writer,
        prompt_re=SNR_PROMPT_RE,
        timeout=0.5,
    )

    # ==========================
    # S2985G-48T and S2990G-48T — FLASH LOGGING
    # ==========================
    if model in ("S2985G-48T", "S2990G-48T"):
        writer.write(SHOW_LOGGING_FLASH + "\n")

        log_re = re.compile(
            rf"""
            ^(?P<id>\d+)\s+
            (?P<time>%[A-Za-z]+\s+\d+\s+\d+:\d+:\d+).*?
            Line\s+protocol\s+on\s+Interface\s+{re.escape(iface)},\s+
            changed\s+state\s+to\s+(?P<event>UP|DOWN)
            """,
            re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        )

        buf = ""
        max_lines = 200

        while True:
            chunk = await reader.read(16384)
            if not chunk:
                break

            if "--More--" in chunk:
                writer.write(" ")
                chunk = chunk.replace("--More--", "")

            buf += chunk

            # основной ограничитель
            if buf.count("\n") >= max_lines:
                break

            # вторичный — на случай короткого вывода
            if chunk.rstrip().endswith("#"):
                break

        for m in log_re.finditer(buf):
            logs.append(
                f"{m.group('id')} "
                f"{m.group('time').lstrip('%')} "
                f"{iface} "
                f"{m.group('event').upper()}"
            )
            if len(logs) >= limit:
                break

    # ==========================
    # ALL OTHER MODELS — INCLUDE
    # ==========================
    else:
        port_num = port.split("/")[-1]
        writer.write(
            SHOW_LOGGING_INCLUDE.format(port_num=port_num) + "\n"
        )

        buf = await read_until_prompt(
            reader,
            writer,
            prompt_re=SNR_PROMPT_RE,
            timeout=1.0,
        )

        include_re = re.compile(
            rf"""
            ^(?P<id>\d+)\s+
            (?P<time>%[A-Za-z]+\s+\d+\s+\d+:\d+:\d+).*?
            {re.escape(iface)}.*?
            (?P<event>UP|DOWN)
            """,
            re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        )

        for m in include_re.finditer(buf):
            logs.append(
                f"{m.group('id')} "
                f"{m.group('time').lstrip('%')} "
                f"{iface} "
                f"{m.group('event').upper()}"
            )
            if len(logs) >= limit:
                break

    # ==========================
    # restore terminal
    # ==========================
    writer.write("terminal length 0\n")
    await read_until_prompt(
        reader,
        writer,
        prompt_re=SNR_PROMPT_RE,
        timeout=0.5,
    )

    return logs
