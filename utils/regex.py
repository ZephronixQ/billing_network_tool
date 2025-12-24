import re

ANSI = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

UNCFG_ONU = re.compile(
    r'gpon-onu_(\d+/\d+/\d+):\d+\s+([A-Z0-9]{8,})\s+unknown',
    re.I
)
