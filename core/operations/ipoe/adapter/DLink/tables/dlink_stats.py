from output.colors import CYAN, YELLOW, MAGENTA, RESET, BLUE
from output.table_base import render_table

def print_port_stats(info: dict):
    traffic = info.get("traffic", {})
    errors = info.get("errors", {})

    rows = [[
        f"{CYAN}{traffic.get('rx_bytes', 0)}{RESET}",
        f"{CYAN}{traffic.get('tx_bytes', 0)}{RESET}",
        f"{YELLOW}{errors.get('rx_crc', 0)}{RESET}",
        f"{YELLOW}{errors.get('tx_crc', 0)}{RESET}",
    ]]

    render_table(
        rows=rows,
        headers=[
            f"{BLUE}RX BYTES{RESET}",
            f"{BLUE}TX BYTES{RESET}",
            f"{BLUE}RX ERR{RESET}",
            f"{BLUE}TX ERR{RESET}",
        ],
        title=f"{MAGENTA}\n📊 PORT COUNTERS{RESET}",
    )
