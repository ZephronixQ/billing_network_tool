from output.colors import BLUE, CYAN, MAGENTA, YELLOW, RESET
from output.table_base import render_table
from core.operations.ipoe.adapter.SNR.constants import SNR_MODEL_PORTS, format_ports


def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"


def print_device_info(model: str):
    fe, ge = SNR_MODEL_PORTS.get(model, (0, 0))
    ports_str = format_ports(fe, ge)

    headers = [
        f"{BLUE}VENDOR{RESET}",
        f"{BLUE}MODEL{RESET}",
        f"{BLUE}PORTS{RESET}",
    ]

    rows = [[
        _c("SNR", CYAN),
        _c(model, MAGENTA),
        _c(ports_str, YELLOW),
    ]]

    render_table(
        rows=rows,
        headers=headers,
        title=f"\n{MAGENTA}🖥 DEVICE INFO{RESET}",
    )
