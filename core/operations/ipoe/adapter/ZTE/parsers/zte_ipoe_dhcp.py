import re
from core.operations.ipoe.common.utils import mac_to_plain

def parse_dhcp_relay(raw: str) -> list[dict]:
    bindings = []

    dhcp_re = re.compile(
        r'(?P<mac>(?:[0-9a-f]{2}\.){5}[0-9a-f]{2})\s+'
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
        r'\d+\s+'
        r'(?P<vlan>\d+)\s+'
        r'(?P<port>\d+)',
        re.I
    )

    for line in raw.splitlines():
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
