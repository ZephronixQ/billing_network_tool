import re

from core.operations.ipoe.adapter.ELTEX.constants import (
    ELTEX_PROMPT_RE,
    DEFAULT_LOG_LINES,
)


def parse_logs(
    output: str,
    short_port: str,
    max_lines: int = DEFAULT_LOG_LINES,
) -> list[str]:
    lines = []
    port_re = re.compile(rf"\b{re.escape(short_port)}\b", re.I)

    for raw in output.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("show logging"):
            continue
        if ELTEX_PROMPT_RE.match(line):
            continue
        if line.startswith("More:"):
            continue
        if port_re.search(line):
            lines.append(line)
        if len(lines) >= max_lines:
            break

    return lines
