from output.colors import GREEN, RED, CYAN, YELLOW, RESET, MAGENTA
from output.table_base import render_table
import re


LOG_RE = re.compile(
    r"(?P<time>\w+\s+\w+\s+\d+\s+\d+:\d+:\d+\s+\d+).*Port\s*:\s*(?P<port>\d+)\s+(?P<event>\w+)",
    re.IGNORECASE
)


def print_logs(logs: list[str]):
    print()

    # ===== NO LOGS =====
    if not logs:
        print(f"{CYAN}📜 DEVICE LOGS{RESET}")
        print(f"{YELLOW}Нет логов для данного порта{RESET}")
        return

    rows = []

    for log in logs:
        match = LOG_RE.search(log)

        if not match:
            rows.append([
                f"{CYAN}{log}{RESET}",
                "-",
                "-",
            ])
            continue

        time = f"{YELLOW}{match.group('time')}{RESET}"
        port = f"{MAGENTA}{match.group('port')}{RESET}"
        event = match.group("event").lower()

        if "down" in event:
            event_colored = f"{RED}{event}{RESET}"
        elif "up" in event:
            event_colored = f"{GREEN}{event}{RESET}"
        else:
            event_colored = f"{YELLOW}{event}{RESET}"

        rows.append([
            time,
            port,
            event_colored,
        ])

    render_table(
        rows=rows,
        headers=[
            f"{CYAN}TIME{RESET}",
            f"{CYAN}PORT{RESET}",
            f"{CYAN}EVENT{RESET}",
        ],
        title=f"{CYAN}📜 DEVICE LOGS{RESET}",
    )
