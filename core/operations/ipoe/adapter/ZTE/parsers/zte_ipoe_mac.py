import re
from core.operations.ipoe.common.utils import mac_to_plain

def parse_zte_mac(raw: str) -> list[dict]:
    table = []

    mac_re = re.compile(
        r'(?P<mac>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}).*?'
        r'port-(?P<port>\d+).*?'
        r'(?P<time>\d+:\d+:\d+:\d+)',
        re.I
    )

    vlan_re = re.compile(
        r'(?P<mac>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+(?P<vlan>\d+)',
        re.I
    )

    for line in raw.splitlines():
        m = mac_re.search(line)
        v = vlan_re.search(line)

        if not m or not v:
            continue

        table.append({
            "mac": m.group("mac").lower(),
            "mac_plain": mac_to_plain(m.group("mac")),
            "vlan": v.group("vlan"),
            "port": m.group("port"),
            "time": m.group("time"),
        })

    return table
