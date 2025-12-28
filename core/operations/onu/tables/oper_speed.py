from output.colors import (
    GREEN, RED, CYAN, MAGENTA, BLUE, RESET
)
from output.table_base import render_table


def print_oper_speed_table(remote_onu: dict, iface_speed: dict):
    headers = [
        f"{BLUE}Operate status{RESET}",
        f"{BLUE}Speed status{RESET}",
        f"{BLUE}Input rate (Mbit/s){RESET}",
        f"{BLUE}Output rate (Mbit/s){RESET}",
    ]

    rows = [[
        f"{GREEN if remote_onu['operate'].lower() == 'enable' else RED}"
        f"{remote_onu['operate']}{RESET}",

        f"{GREEN if remote_onu['speed'].lower() != 'disable' else RED}"
        f"{remote_onu['speed']}{RESET}",

        f"{CYAN}{iface_speed['input_mbps']}{RESET}",
        f"{MAGENTA}{iface_speed['output_mbps']}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}⚡ OPERATE / SPEED / THROUGHPUT{RESET}",
    )
