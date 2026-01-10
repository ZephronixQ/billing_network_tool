import re

def parse_port_bytes(lines: list[str]):
    rx_bytes = 0
    tx_bytes = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        columns = re.split(r'\s+', line)

        # RX Bytes
        if "RX Bytes" in line:
            try:
                idx = columns.index("RX")
                rx_bytes = int(columns[idx + 3])
            except (ValueError, IndexError):
                pass

        # TX Bytes
        if "TX Bytes" in line:
            try:
                idx = columns.index("TX")
                tx_bytes = int(columns[idx + 3])
            except (ValueError, IndexError):
                pass

    return rx_bytes, tx_bytes
