from output.colors import BLUE, RED, RESET
from output.table_base import render_table


def print_port_errors(iface: dict):
    headers = [
        f"{BLUE}INPUT ERRORS{RESET}",
        f"{BLUE}OUTPUT ERRORS{RESET}",
    ]

    rows = [[
        f"{RED}{iface.get('input_errors', '0')}{RESET}",
        f"{RED}{iface.get('output_errors', '0')}{RESET}",
    ]]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{BLUE}⚠ ERRORS{RESET}",
    )
