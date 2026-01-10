import re

MAC_RE = re.compile(
    r'(?P<vid>\d+)\s+\S+\s+'
    r'(?P<mac>(?:[0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2})'
)

def parse_port_macs(lines: list[str]) -> list[dict]:
    macs = []

    for line in lines:
        m = MAC_RE.search(line)
        if not m:
            continue

        macs.append({
            "vid": int(m.group("vid")),
            "mac": m.group("mac").upper(),
        })

    return macs
