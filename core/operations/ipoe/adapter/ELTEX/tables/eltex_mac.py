from output.colors import BLUE, CYAN, YELLOW, RESET
from output.table_base import render_table


def print_mac(macs: list[dict]):
    if not macs:
        print(f"\n{YELLOW}⚠ MAC не найдены{RESET}")
        return

    headers = [
        f"{BLUE}VLAN{RESET}",
        f"{BLUE}MAC{RESET}",
        f"{BLUE}TYPE{RESET}",
    ]

    rows = [
        [
            m.get("vlan"),
            f"{CYAN}{m.get('mac')}{RESET}",
            m.get("type"),
        ]
        for m in macs
    ]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{BLUE}📡 MAC TABLE{RESET}",
    )
