from output.table_base import render_table
from output.colors import GREEN, RED, CYAN, MAGENTA, YELLOW, BLUE, RESET

DOWN_RX_WARN_THRESHOLD = 28.0  # dBm

def print_pon_power_table(rows):
    if not rows:
        return

    table_rows = []
    warnings = []

    headers = [
        f"{BLUE}DIR{RESET}",
        f"{BLUE}OLT{RESET}",
        f"{BLUE}ONU{RESET}",
        f"{BLUE}ATTENUATION{RESET}",
    ]

    for r in rows:
        table_rows.append([
            f"{GREEN if r['direction']=='UP' else RED}{r['direction']}{RESET}",
            f"{CYAN}{r['olt']}{RESET}",
            f"{MAGENTA}{r['onu']}{RESET}",
            f"{YELLOW}{r['attenuation']}{RESET}",
        ])

        if r["direction"] == "DOWN" and r["onu_rx"] is not None:
            if r["onu_rx"] > DOWN_RX_WARN_THRESHOLD:
                warnings.append(r["onu_rx"])

    render_table(
        rows=table_rows,
        headers=headers,
        title=f"\n{CYAN}📡 PON POWER LEVELS{RESET}",
    )

    for rx in warnings:
        print(f"{RED}WARNING:{RESET} LOW DOWNSTREAM SIGNAL — -{rx} dBm")
