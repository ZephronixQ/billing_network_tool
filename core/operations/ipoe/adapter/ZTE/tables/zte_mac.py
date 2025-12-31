from output.colors import GREEN, BLUE, YELLOW, MAGENTA, CYAN, RED, RESET
from output.table_base import render_table


def print_mac_table(mac_entry: dict | None):
    headers = [
        f"{BLUE}MAC ADDRESS{RESET}",
        f"{BLUE}VLAN{RESET}",
        f"{BLUE}PORT{RESET}",
        f"{BLUE}AGE{RESET}",
    ]

    if not mac_entry:
        rows = [[
            f"{RED}NOT FOUND{RESET}",
            "-",
            "-",
            "-",
        ]]

        render_table(
            rows,
            headers,
            title=f"\n{RED}❌ MAC NOT FOUND{RESET}",
        )
        return

    rows = [[
        f"{GREEN}{mac_entry['mac']}{RESET}",
        f"{YELLOW}{mac_entry.get('vlan', 'N/A')}{RESET}",
        f"{MAGENTA}{mac_entry['port']}{RESET}",
        f"{CYAN}{mac_entry['time']}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}✅ MAC FOUND{RESET}",
    )
