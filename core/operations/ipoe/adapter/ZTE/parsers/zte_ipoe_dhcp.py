import re
from core.operations.ipoe.common.utils import mac_to_plain

def parse_dhcp_relay(raw: str) -> list[dict]:
    bindings = []

    # регулярка для нового формата: Port Vlan IP MAC Lease Status
    dhcp_re = re.compile(
        r'(?P<port>\d+)\s+'
        r'(?P<vlan>\d+)\s+'
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
        r'(?P<mac>(?:[0-9a-f]{2}\.){5}[0-9a-f]{2})',
        re.I
    )

    for line in raw.splitlines():
        line = line.strip()
        # пропускаем заголовки и пустые строки
        if not line or line.startswith("Port") or line.startswith("----"):
            continue

        m = dhcp_re.search(line)
        if not m:
            continue

        bindings.append({
            "mac": m.group("mac").lower(),
            "mac_plain": mac_to_plain(m.group("mac")),
            "ip": m.group("ip"),
            "vlan": m.group("vlan"),
            "port": m.group("port"),
        })

    return bindings
