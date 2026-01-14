from output.colors import GREEN, BLUE, YELLOW, MAGENTA, CYAN, RED, RESET
from output.table_base import render_table

def print_mac_table(mac_entry: dict | list | None):
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

        info = [
            f"{YELLOW}Возможные причины:{RESET}",
            f"{YELLOW}- Устройство не настроено/сброшено{RESET}",
        ]
        print("\n".join(info))
        return

    # Если передан список (MAC найден на нескольких портах)
    if isinstance(mac_entry, list):
        rows = []
        for entry in mac_entry:
            rows.append([
                f"{GREEN}{entry['mac']}{RESET}",
                f"{YELLOW}{entry.get('vlan', 'N/A')}{RESET}",
                f"{MAGENTA}{entry['port']}{RESET}",
                f"{CYAN}{entry.get('time', '-')}{RESET}",
            ])

        render_table(
            rows,
            headers,
            title=f"\n{CYAN}⚠ MAC FOUND MULTIPLE PORTS{RESET}",
        )

        print(f"{RED}⚠ Внимание: на одном порту найдено несколько MAC адресов!{RESET}")
        print(f"{YELLOW}- Возможная ошибка: абонент перепутал порты WAN и LAN на роутере{RESET}")
        return

    # Один MAC найден
    rows = [[
        f"{GREEN}{mac_entry['mac']}{RESET}",
        f"{YELLOW}{mac_entry.get('vlan', 'N/A')}{RESET}",
        f"{MAGENTA}{mac_entry['port']}{RESET}",
        f"{CYAN}{mac_entry.get('time', '-')}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}✅ MAC FOUND{RESET}",
    )
