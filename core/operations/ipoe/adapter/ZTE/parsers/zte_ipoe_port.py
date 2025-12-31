import re
from core.operations.ipoe.common.utils import extract

def parse_port_info(output: str) -> dict:
    ps = re.search(
        r'PortStatus\s*:\s*(.*?)(?:\n\S|\Z)',
        output,
        re.I | re.S
    )

    if not ps:
        return {
            "state": "N/A",
            "speed": "N/A",
        }

    block = ps.group(1)

    state = extract(r'Link\s*:\s*(up|down)', block).upper()

    speed_match = re.search(
        r'Speed\s*:\s*(\d+)\s*(M|G)bps',
        block,
        re.I
    )

    speed = (
        f"{speed_match.group(1)}{speed_match.group(2).upper()}bps"
        if speed_match else "N/A"
    )

    return {
        "state": state,
        "speed": speed,
    }


def parse_port_errors(statistics: str) -> dict:
    return {
        "in_err": extract(r'InMACRcvErr\s*:\s*(\d+)', statistics, "0"),
        "crc": extract(r'CrcError\s*:\s*(\d+)', statistics, "0"),
    }


def parse_mac_protect(raw: str, port: str) -> dict:
    """
    Парсит вывод:
    show mac protect port X
    """

    for line in raw.splitlines():
        cols = line.split()

        # ожидаем строку вида:
        # port-12 Enable No Restrict
        if len(cols) >= 4 and cols[0] == f"port-{port}":
            return {
                "enabled": cols[1].lower() == "enable",
                "active": cols[2].lower() == "yes",
                "action": cols[3],
            }

    return {
        "enabled": False,
        "active": False,
        "action": "N/A",
    }

