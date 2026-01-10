from output.colors import CYAN, MAGENTA, YELLOW, RESET, BLUE, RED, GREEN
from output.table_base import render_table
import re

def print_logs(info: dict):
    logs = info.get("logs", [])

    log_re = re.compile(r"(\d+)\s+([A-Za-z]+\s+\d+\s+[\d:]+):.*Port\s+(\d+)\s+(.*)", re.IGNORECASE)

    rows = []

    if not logs:
        rows.append([f"No logs"])
        headers = [f"{BLUE}EVENT{RESET}"]
    else:
        for log in logs:
            m = log_re.match(log)
            if m:
                log_id, log_time, port, event = m.groups()
                event = re.sub(r"LinkStatus-?\d+: ?", "", event, flags=re.IGNORECASE)

                def color_event(text):
                    text = text.strip()
                    if re.search(r"link up", text, re.IGNORECASE):
                        return f"{GREEN}{text}{RESET}"
                    elif re.search(r"link down", text, re.IGNORECASE):
                        return f"{RED}{text}{RESET}"
                    else:
                        return text

                colored_event = color_event(event)

                rows.append([
                    f"{CYAN}{log_id}{RESET}",
                    f"{MAGENTA}{log_time}{RESET}",
                    f"{YELLOW}{port}{RESET}",
                    colored_event
                ])
        headers = [
            f"{BLUE}ID{RESET}",
            f"{BLUE}TIME{RESET}",
            f"{BLUE}PORT{RESET}",
            f"{BLUE}EVENT{RESET}"
        ]

    render_table(
        rows=rows,
        headers=headers,
        title=f"{MAGENTA}\n📜 DEVICE LOGS{RESET}"
    )
