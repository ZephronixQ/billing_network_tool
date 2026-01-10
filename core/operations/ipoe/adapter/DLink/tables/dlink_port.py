from output.colors import CYAN, GREEN, YELLOW, MAGENTA, RESET, BLUE
from output.table_base import render_table

def print_port_status(port: int | None, info: dict):
    port_id = info.get("port", port if port is not None else "N/A")
    port_state = info.get("port_state", "N/A")
    port_speed = info.get("port_speed") or "N/A"

    rows = [[
        f"{CYAN}{port_id}{RESET}",
        f"{GREEN}{port_state}{RESET}",
        f"{YELLOW}{port_speed}{RESET}",
    ]]

    render_table(
        rows=rows,
        headers=[
            f"{BLUE}PORT{RESET}",
            f"{BLUE}STATE{RESET}",
            f"{BLUE}SPEED{RESET}",
        ],
        title=f"{MAGENTA}\n🔌 PORT STATUS{RESET}",
    )
