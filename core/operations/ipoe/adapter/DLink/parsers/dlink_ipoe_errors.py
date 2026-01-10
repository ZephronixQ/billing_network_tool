import re

def parse_port_errors(lines: list[str]):
    rx_crc = 0
    tx_crc = 0
    rx_desc = ""
    tx_desc = ""

    for line in lines:
        line = line.strip()
        if "CRC Error" in line:
            # ищем числа после 'CRC Error'
            numbers = re.findall(r'CRC Error\s+(\d+)', line)

            if len(numbers) >= 2:
                rx_crc = int(numbers[0])
                tx_crc = int(numbers[1])
                rx_desc = f"CRC Error {rx_crc}"
                tx_desc = f"CRC Error {tx_crc}"
                break  # как в оригинале, останавливаемся на первой строке

            elif len(numbers) == 1:
                rx_crc = int(numbers[0])
                rx_desc = f"CRC Error {rx_crc}"
                # tx_crc остаётся 0
                break  # тоже останавливаемся на первой строке

    return rx_crc, tx_crc, rx_desc, tx_desc
