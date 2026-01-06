# core/operations/ipoe/adapter/ELTEX/tables/eltex_stats.py

from output.colors import BLUE, CYAN, RED, RESET
from output.table_base import render_table


def print_port_stats(iface: dict):
    headers = [
        f"{BLUE}IN (Kbit/s){RESET}",
        f"{BLUE}OUT (Kbit/s){RESET}",
        f"{BLUE}IN ERR{RESET}",
        f"{BLUE}OUT ERR{RESET}",
    ]

    rows = [[
        f"{CYAN}{iface.get('input_rate', '0')}{RESET}",
        f"{CYAN}{iface.get('output_rate', '0')}{RESET}",
        f"{RED}{iface.get('input_errors', '0')}{RESET}",
        f"{RED}{iface.get('output_errors', '0')}{RESET}",
    ]]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{BLUE}📊 TRAFFIC & ERRORS{RESET}",
    )
