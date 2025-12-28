import re
from .common import clean_line

RX_RE  = re.compile(r"Rx\s*:?[\s]*(-?\d+(?:\.\d+)?)", re.I)
TX_RE  = re.compile(r"Tx\s*:?[\s]*(-?\d+(?:\.\d+)?)", re.I)
ATT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*\(d[bB]\)", re.I)


def parse_pon_power(output: str):
    if not output:
        return []

    rows = []

    for raw in output.splitlines():
        line = clean_line(raw)
        if not line:
            continue

        parts = line.split()
        if not parts:
            continue

        first = parts[0].lower()

        if first == "up":
            direction = "UP"
        elif first == "down":
            direction = "DOWN"
        else:
            continue

        rx = RX_RE.search(line)
        tx = TX_RE.search(line)
        att = ATT_RE.search(line)

        if not (rx and tx and att):
            continue

        rx_val = float(rx.group(1))
        tx_val = float(tx.group(1))
        att_val = att.group(1)

        if direction == "UP":
            olt = f"Rx {rx_val} dBm"
            onu = f"Tx {tx_val} dBm"
            onu_rx = None
        else:
            olt = f"Tx {tx_val} dBm"
            onu = f"Rx {rx_val} dBm"
            onu_rx = abs(rx_val)

        rows.append({
            "direction": direction,
            "olt": olt,
            "onu": onu,
            "attenuation": att_val,
            "onu_rx": onu_rx,
        })

    return rows
