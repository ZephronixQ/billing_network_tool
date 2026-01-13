from output.colors import BLUE, CYAN, MAGENTA, YELLOW, RESET
from output.table_base import render_table

def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"

def print_device_info(dev: dict):
    vendor = dev.get("vendor", "N/A")
    model = dev.get("model", "N/A")
    ports_raw = dev.get("ports")

    if isinstance(ports_raw, dict):
        fe = ports_raw.get("fe", 0)
        ge = ports_raw.get("ge", 0)
        total = fe + ge
        ports_str = f"{fe}FE + {ge}GE ({total})"

    elif isinstance(ports_raw, int):
        ports_str = f"{ports_raw}"

    else:
        ports_str = "N/A"

    headers = [
        f"{BLUE}VENDOR{RESET}",
        f"{BLUE}MODEL{RESET}",
        f"{BLUE}PORTS{RESET}",
    ]

    rows = [[
        _c(vendor, CYAN),
        _c(model, MAGENTA),
        _c(ports_str, YELLOW),
    ]]
    
    render_table(
        rows,
        headers,
        title=f"\n{MAGENTA}🖥 DEVICE INFO{RESET}",
    )
