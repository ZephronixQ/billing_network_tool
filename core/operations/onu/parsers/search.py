import re
from .common import clean_line

GPON_SN_REGEX = re.compile(r'gpon-onu_(\d+/\d+/\d+:\d+)', re.I)

REMOTE_ID_REGEX = re.compile(
    r'port-(?:location|identification)\s+sub-option\s+remote-id\s+name\s+(\S+)',
    re.I
)

def parse_onu_interface(output: str):
    for line in output.splitlines():
        m = GPON_SN_REGEX.search(clean_line(line))
        if m:
            return m.group(1)
    return None

def parse_remote_id(output: str):
    for line in output.splitlines():
        m = REMOTE_ID_REGEX.search(clean_line(line))
        if m:
            return m.group(1)
    return None
