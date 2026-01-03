from output.colors import BLUE, CYAN, MAGENTA, YELLOW, RESET, GREEN
from output.table_base import render_table


def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_mac(mac: dict | None):
    headers = [
        f"{BLUE}MAC{RESET}",
        f"{BLUE}VLAN{RESET}",
    ]

    if not mac:
        render_table(
            [["—", "—"]],
            headers,
            title=f"{MAGENTA}❌ MAC NOT FOUND{RESET}",
        )
        return

    rows = [[
        _c(mac["mac"], CYAN),
        _c(str(mac["vlan"]), YELLOW),
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{GREEN}✅ MAC FOUND{RESET}",
    )
