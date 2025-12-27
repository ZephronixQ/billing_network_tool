from output.colors import CYAN, MAGENTA, YELLOW, BLUE, RESET
from output.table_base import render_table

def print_ip_status(ip_service: dict):
    headers = [
        f"{BLUE}IP{RESET}",
        f"{BLUE}MAC{RESET}",
        f"{BLUE}VLAN{RESET}",
    ]

    rows = [[
        f"{CYAN}{ip_service['ip']}{RESET}",
        f"{MAGENTA}{ip_service['mac']}{RESET}",
        f"{YELLOW}{ip_service['vlan']}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}🌐 IP STATUS{RESET}",
    )
