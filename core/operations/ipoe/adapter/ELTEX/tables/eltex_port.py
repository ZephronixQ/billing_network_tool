from output.colors import BLUE, GREEN, RED, RESET
from output.table_base import render_table


def _status(val: str) -> str:
    color = GREEN if val == "up" else RED
    return f"{color}{val.upper()}{RESET}"


def print_port_status(port: int, iface: dict) -> bool:
    status = iface.get("status", "down")

    headers = [
        f"{BLUE}PORT{RESET}",
        f"{BLUE}STATUS{RESET}",
    ]

    rows = [[
        str(port),
        _status(status),
    ]]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{BLUE}🔌 PORT STATE{RESET}",
    )

    return status == "up"
