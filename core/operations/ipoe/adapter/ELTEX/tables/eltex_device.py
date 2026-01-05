from output.colors import BLUE, CYAN, MAGENTA, YELLOW, RESET
from output.table_base import render_table

def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_device_info(device: dict):
    headers = [
        f"{BLUE}VENDOR{RESET}",
        f"{BLUE}MODEL{RESET}",
        f"{BLUE}PORTS{RESET}",
        f"{BLUE}SPEED{RESET}",
    ]

    rows = [[
        _c(device.get("vendor", "ELTEX"), CYAN),
        _c(device.get("model", "UNKNOWN"), MAGENTA),
        _c(str(device.get("ports", "?")), YELLOW),
        _c(device.get("speed", "?"), YELLOW),
    ]]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{MAGENTA}🖥 DEVICE INFO{RESET}",
    )
