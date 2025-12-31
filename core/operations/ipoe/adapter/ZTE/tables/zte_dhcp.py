from output.colors import GREEN, BLUE, YELLOW, MAGENTA, RED, RESET
from output.table_base import render_table


def print_dhcp(dhcp_entry: dict | None):
    headers = [
        f"{BLUE}IP ADDRESS{RESET}",
        f"{BLUE}VLAN{RESET}",
        f"{BLUE}PORT{RESET}",
    ]

    if not dhcp_entry:
        rows = [[
            f"{RED}NOT FOUND{RESET}",
            "-",
            "-",
        ]]

        render_table(
            rows,
            headers,
            title=f"\n{RED}❌ DHCP NOT FOUND{RESET}",
        )
        return

    rows = [[
        f"{GREEN}{dhcp_entry['ip']}{RESET}",
        f"{YELLOW}{dhcp_entry['vlan']}{RESET}",
        f"{MAGENTA}{dhcp_entry['port']}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{GREEN}✅ DHCP BINDING{RESET}",
    )
