import re
from .common import clean_line

IP_SERVICE_RE = re.compile(r'^\d+\s+\d+\.\d+\.\d+\.\d+')
DHCP_SNOOP_RE = re.compile(
    r'^\d+\s+([0-9A-Fa-f.]+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+dynamic',
)

EMPTY = {
    "ip": "-",
    "mac": "-",
    "vlan": "-",
}

def parse_ip_status(output: str) -> dict:
    for raw in output.splitlines():
        line = clean_line(raw)

        # === DHCP SNOOPING FORMAT ===
        m = DHCP_SNOOP_RE.match(line)
        if m:
            mac, ip, vlan = m.groups()
            return {
                "ip": ip,
                "mac": mac,
                "vlan": vlan,
            }

        # === IP-SERVICE FORMAT ===
        if IP_SERVICE_RE.match(line):
            parts = line.split()
            if len(parts) >= 4:
                return {
                    "ip": parts[1],
                    "mac": parts[2],
                    "vlan": parts[3],
                }

    return EMPTY
