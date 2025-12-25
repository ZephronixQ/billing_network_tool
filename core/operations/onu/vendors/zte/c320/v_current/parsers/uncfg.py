import re
from .common import clean_line

UNCFG_REGEX = re.compile(
    r'gpon-onu_(\d+/\d+/\d+):\d+\s+([A-Z0-9]{8,})\s+unknown',
    re.I
)

def parse_uncfg(output: str):
    result = []
    for line in output.splitlines():
        line = clean_line(line)
        if not line:
            continue
        m = UNCFG_REGEX.search(line)
        if m:
            result.append({
                "port": m.group(1),
                "serial": m.group(2),
            })
    return result
