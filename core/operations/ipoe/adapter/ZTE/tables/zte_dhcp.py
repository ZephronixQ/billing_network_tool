from output.colors import GREEN, BLUE, YELLOW, MAGENTA, RED, CYAN, RESET
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

        # Возможные причины и рекомендации
        dhcp_info = [
            f"{YELLOW}Возможные причины:{RESET}",
            f"{YELLOW}- Проблемы с клиентским роутером{RESET}",
            f"{YELLOW}- VLAN на порту не соответствует DHCP пулу{RESET}",

        ]
        print("\n".join(dhcp_info))
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
