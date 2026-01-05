from output.colors import BLUE, CYAN, RESET
from output.table_base import render_table


def print_port_traffic(iface: dict):
    headers = [
        f"{BLUE}INPUT (Kbit/s){RESET}",
        f"{BLUE}OUTPUT (Kbit/s){RESET}",
    ]

    rows = [[
        f"{CYAN}{iface.get('input_rate', '0')}{RESET}",
        f"{CYAN}{iface.get('output_rate', '0')}{RESET}",
    ]]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{BLUE}📊 TRAFFIC{RESET}",
    )
