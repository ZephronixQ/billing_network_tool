import re
from .common import clean_line

GPON_SN_REGEX = re.compile(r'gpon-onu_(\d+/\d+/\d+:\d+)', re.I)
REMOTE_ID_REGEX = re.compile(
    r'port-location sub-option remote-id name (\S+) vport',
    re.I
)

def parse_onu_interface(output: str):
    for line in output.splitlines():
        line = clean_line(line)
        m = GPON_SN_REGEX.search(line)
        if m:
            return m.group(1)
    return None

def parse_remote_id(output: str):
    for line in output.splitlines():
        line = clean_line(line)
        m = REMOTE_ID_REGEX.search(line)
        if m:
            return m.group(1)
    return None
