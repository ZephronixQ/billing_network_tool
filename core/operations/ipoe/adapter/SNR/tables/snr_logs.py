# core/operations/ipoe/adapter/SNR/tables/snr_logs.py

from output.colors import BLUE, CYAN, YELLOW, RESET
from output.table_base import render_table


def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_logs(logs: list[str]):
    title = f"\n{CYAN}📜 DEVICE LOGS{RESET}"

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
        # ожидаемый формат:
        # "618 %Jan 01 00:00:26 - DOWN"
        try:
            left, event = line.split("-", 1)
            event = event.strip()

            parts = left.strip().split(maxsplit=1)
            log_id = parts[0]
            time = parts[1].lstrip("%")

        except Exception:
            continue

        # 🔑 дедупликация строго по ID
        if log_id in seen_ids:
            continue

        seen_ids.add(log_id)

        rows.append([
            _c(log_id, CYAN),
            time,
            _c(event, YELLOW if event == "UP" else RESET),
        ])

    headers = [
        f"{BLUE}ID{RESET}",
        f"{BLUE}TIME{RESET}",
        f"{BLUE}EVENT{RESET}",
    ]

    render_table(
        rows=rows,
        headers=headers,
        title=title,
    )
