import re

ANSI = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

UNCFG_REGEX = re.compile(
    r'gpon-onu_(\d+/\d+/\d+):\d+\s+([A-Z0-9]{8,})\s+unknown',
    re.I
)

# --- ONU by serial ---
GPON_SN_REGEX = re.compile(
    r'gpon-onu_(\d+/\d+/\d+:\d+)',
    re.I
)

REMOTE_ID_REGEX = re.compile(
    r'port-location sub-option remote-id name (\S+) vport',
    re.I
)