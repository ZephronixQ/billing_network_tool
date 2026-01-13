from output.colors import BLUE, CYAN, GREEN, RED, RESET
from output.table_base import render_table

def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"

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
    seen_ids: set[str] = set()

    for line in logs:
        try:
            parts = line.split()

            # ===== NEW FORMAT =====
            if len(parts) >= 5:
                log_id = parts[0]
                time = " ".join(parts[1:4])
                iface = parts[4]
                event = parts[5] if len(parts) > 5 else parts[-1]

            # ===== OLD FORMAT 2 =====
            elif "-" in line and line.count("-") == 2:
                log_id, iface, event = [p.strip() for p in line.split("-")]
                time = ""

            # ===== OLD FORMAT 1 =====
            elif "-" in line:
                left, event = [p.strip() for p in line.split("-", 1)]
                left_parts = left.split(maxsplit=1)
                log_id = left_parts[0]
                time = left_parts[1].lstrip("%") if len(left_parts) > 1 else ""
                iface = ""

            else:
                continue

            event = event.upper()

        except Exception:
            continue

        if log_id in seen_ids:
            continue
        seen_ids.add(log_id)

        event_color = GREEN if event == "UP" else RED

        rows.append([
            _c(log_id, CYAN),
            _c(time, BLUE) if time else "",
            _c(iface, CYAN) if iface else "",
            _c(event, event_color),
        ])

    headers = [
        f"{BLUE}ID{RESET}",
        f"{BLUE}TIME{RESET}",
        f"{BLUE}IFACE{RESET}",
        f"{BLUE}EVENT{RESET}",
    ]

    render_table(
        rows=rows,
        headers=headers,
        title=title,
    )
