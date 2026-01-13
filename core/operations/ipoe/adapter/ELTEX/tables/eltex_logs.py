from output.colors import BLUE, CYAN, GREEN, RED, RESET
from output.table_base import render_table
import re

def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"

LOG_RE = re.compile(
    r"""
    (?P<date>\d{2}-[A-Za-z]{3}-\d{4})\s+
    (?P<time>\d{2}:\d{2}:\d{2})\s+
    :%LINK-\w-(?P<event>UP|DOWN):\s+
    (?P<iface>\S+)
    """,
    re.VERBOSE | re.IGNORECASE,
)

def print_logs(logs: list[str]):
    title = f"\n{CYAN}📜 DEVICE LOGS (MAX LINES = 200){RESET}"

    if not logs:
        render_table(
            rows=[["No logs found"]],
            headers=[f"{BLUE}INFO{RESET}"],
            title=title,
        )
        return

    rows: list[list[str]] = []

    for line in logs:
        m = LOG_RE.search(line)
        if not m:
            continue

        date = m.group("date")
        time = m.group("time")
        iface = m.group("iface").lower()
        event = m.group("event").upper()

        color = GREEN if event == "UP" else RED

        rows.append([
            _c(date, CYAN),
            _c(time, BLUE),
            _c(iface, CYAN),
            _c(event, color),
        ])

    if not rows:
        render_table(
            rows=[["Logs found, but parsing failed"]],
            headers=[f"{BLUE}INFO{RESET}"],
            title=title,
        )
        return

    headers = [
        f"{BLUE}DATE{RESET}",
        f"{BLUE}TIME{RESET}",
        f"{BLUE}IFACE{RESET}",
        f"{BLUE}EVENT{RESET}",
    ]

    render_table(
        rows=rows,
        headers=headers,
        title=title,
    )
