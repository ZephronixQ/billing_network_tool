from output.colors import CYAN, GREEN, YELLOW, MAGENTA, RESET, BLUE
from output.table_base import render_table

def format_ports(port_profile: dict) -> str:
    parts = []
    total = 0

    for key, label in (("fe", "FE"), ("ge", "GE"), ("sfp", "SFP")):
        count = port_profile.get(key, 0)
        if count > 0:
            parts.append(f"{count}{label}")
            total += count

    return f"{' + '.join(parts)} ({total})" if parts else "(0)"

def print_device_info(info: dict, port_profile: dict | None = None):
    if not port_profile:
        ports = info.get("ports")
        if isinstance(ports, dict):
            port_profile = {
                k: ports.get(k, 0)
                for k in ("fe", "ge", "sfp")
            }
        else:
            port_profile = {}

    rows = [[
        f"{CYAN}{info.get('vendor', 'N/A')}{RESET}",
        f"{GREEN}{info.get('model', 'N/A')}{RESET}",
        f"{YELLOW}{format_ports(port_profile)}{RESET}",
    ]]

    render_table(
        rows=rows,
        headers=[
            f"{BLUE}VENDOR{RESET}",
            f"{BLUE}MODEL{RESET}",
            f"{BLUE}PORTS{RESET}",
        ],
        title=f"{MAGENTA}\n🖥 DEVICE INFO{RESET}",
    )
