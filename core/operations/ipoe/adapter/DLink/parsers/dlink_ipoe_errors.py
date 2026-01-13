import re

def parse_port_errors(lines: list[str]):
    rx_crc = 0
    tx_crc = 0
    rx_desc = ""
    tx_desc = ""

    for line in lines:
        line = line.strip()
        if "CRC Error" in line:
            numbers = re.findall(r'CRC Error\s+(\d+)', line)

            if len(numbers) >= 2:
                rx_crc = int(numbers[0])
                tx_crc = int(numbers[1])
                rx_desc = f"CRC Error {rx_crc}"
                tx_desc = f"CRC Error {tx_crc}"
                break

            elif len(numbers) == 1:
                rx_crc = int(numbers[0])
                rx_desc = f"CRC Error {rx_crc}"
                break

    return rx_crc, tx_crc, rx_desc, tx_desc
