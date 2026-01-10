from output.colors import CYAN, GREEN, MAGENTA, RESET, BLUE, RED
from output.table_base import render_table

def print_mac(info: dict):
    macs = info.get("macs", [])
    port = info.get("port", "N/A")

    rows = []

    if not macs:
        rows.append([f"{CYAN}{port}{RESET}", "", f"No MAC addresses learned"])
    else:
        rows = [
            [
                f"{CYAN}{port}{RESET}",
                f"{GREEN}{m.get('vid', 'N/A')}{RESET}",
                f"{RED}{m.get('mac', 'N/A')}{RESET}",
            ]
            for m in macs
        ]

    render_table(
        rows=rows,
        headers=[
            f"{BLUE}PORT{RESET}",
            f"{BLUE}VID{RESET}",
            f"{BLUE}MAC{RESET}",
        ],
        title=f"{MAGENTA}\n📎 PORT MAC TABLE{RESET}",
    )
