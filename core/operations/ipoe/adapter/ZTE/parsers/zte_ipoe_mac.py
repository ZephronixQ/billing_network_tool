import re
from core.operations.ipoe.common.utils import mac_to_plain

MAC_LINE_RE = re.compile(
    r'(?P<mac>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+'
    r'(?P<vlan>\d+)\s+'
    r'port-(?P<port>\d+).*?'
    r'(?P<time>\d+:\d+:\d+:\d+)',
    re.I
)

def parse_zte_mac(raw: str) -> list[dict]:
    table = []

    for line in raw.splitlines():
        m = MAC_LINE_RE.search(line)
        if not m:
            continue

        mac = m.group("mac").lower()

        table.append({
            "mac": mac,
            "mac_plain": mac_to_plain(mac),
            "vlan": m.group("vlan"),
            "port": m.group("port"),
            "time": m.group("time"),
        })

    return table
