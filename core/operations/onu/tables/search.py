from output.colors import GREEN, BLUE, YELLOW, MAGENTA, RESET
from output.table_base import render_table

def print_sn_table(data):
    headers = [
        f"{BLUE}IP{RESET}",
        f"{BLUE}PORT{RESET}",
        f"{BLUE}SERIAL{RESET}",
        f"{BLUE}ID{RESET}",
    ]

    rows = [[
        f"{GREEN}{data['host']}{RESET}",
        f"{YELLOW}{data['port']}{RESET}",
        f"{MAGENTA}{data['serial']}{RESET}",
        f"{YELLOW}{data['remote_id']}{RESET}" if data["remote_id"] else "-",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{GREEN}✅ ONU FOUND{RESET}",
    )
