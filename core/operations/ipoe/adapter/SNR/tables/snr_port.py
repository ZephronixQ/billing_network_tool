from output.colors import BLUE, CYAN, GREEN, RED, YELLOW, RESET
from output.table_base import render_table

def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"

def print_port_status(port: str, iface: dict) -> bool:
    state = iface.get("state", "N/A")
    speed = iface.get("speed", "N/A")

    state_color = GREEN if state == "UP" else RED

    headers = [
        f"{BLUE}PORT{RESET}",
        f"{BLUE}STATE{RESET}",
        f"{BLUE}SPEED{RESET}",
    ]

    rows = [[
        _c(port, CYAN),
        _c(state, state_color),
        _c(speed, YELLOW),
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}🔌 PORT STATUS{RESET}",
    )

    if state != "UP":
        print(f"{RED}[L1] Нет линка. Возможна физическая проблема.{RESET}")
        return False

    return True

