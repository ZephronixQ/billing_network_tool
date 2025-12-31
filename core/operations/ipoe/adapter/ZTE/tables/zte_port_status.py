from output.colors import GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, RESET
from output.table_base import render_table


def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_port_status(port: str, info: dict, traffic: dict | None = None):
    state = info.get("state", "N/A")
    speed = info.get("speed", "N/A")

    state_color = GREEN if state == "UP" else RED

    # ===== DOWN PORT =====
    if state != "UP":
        headers = [
            f"{BLUE}PORT{RESET}",
            f"{BLUE}STATE{RESET}",
            f"{BLUE}SPEED{RESET}",
        ]

        rows = [[
            _c(port, YELLOW),
            _c(state, state_color),
            _c(speed, MAGENTA),
        ]]

    # ===== UP PORT =====
    else:
        input_rate = traffic.get("input", "-") if traffic else "-"
        output_rate = traffic.get("output", "-") if traffic else "-"

        headers = [
            f"{BLUE}PORT{RESET}",
            f"{BLUE}STATE{RESET}",
            f"{BLUE}SPEED{RESET}",
            f"{BLUE}INPUT{RESET}",
            f"{BLUE}OUTPUT{RESET}",
        ]

        rows = [[
            _c(port, YELLOW),
            _c(state, state_color),
            _c(speed, MAGENTA),
            _c(input_rate, GREEN),
            _c(output_rate, CYAN),
        ]]

    render_table(
        rows,
        headers,
        title=f"\n{RED}🔌 PORT STATUS{RESET}",
    )
