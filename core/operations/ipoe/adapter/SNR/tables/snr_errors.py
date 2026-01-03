from output.colors import BLUE, RED, YELLOW, RESET
from output.table_base import render_table


def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_port_errors(iface: dict):
    headers = [
        f"{BLUE}INPUT ERR{RESET}",
        f"{BLUE}OUTPUT ERR{RESET}",
        f"{BLUE}CRC{RESET}",
    ]

    rows = [[
        _c(str(iface.get("input_err", 0)), RED),
        _c(str(iface.get("output_err", 0)), RED),
        _c(str(iface.get("crc", 0)), RED),
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{YELLOW}⚠️  PORT ERRORS{RESET}",
    )
