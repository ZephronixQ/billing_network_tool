from output.colors import BLUE, CYAN, YELLOW, RESET
from output.table_base import render_table


def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_port_traffic(iface: dict):
    headers = [
        f"{BLUE}IN (5m){RESET}",
        f"{BLUE}OUT (5m){RESET}",
        f"{BLUE}IN (5s){RESET}",
        f"{BLUE}OUT (5s){RESET}",
    ]

    rows = [[
        _c(f"{iface.get('in_5m')} MB/s", YELLOW),
        _c(f"{iface.get('out_5m')} MB/s", YELLOW),
        _c(f"{iface.get('in_5s')} B/s", CYAN),
        _c(f"{iface.get('out_5s')} B/s", CYAN),
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}📊 PORT TRAFFIC{RESET}",
    )
