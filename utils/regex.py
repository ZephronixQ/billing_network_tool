import re

ANSI = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

UNCFG_ONU = re.compile(
    r'gpon-onu_(\d+/\d+/\d+):\d+\s+([A-Z0-9]{8,})\s+unknown',
    re.I
)


ZTE_DEVICE_RE = re.compile(r'ZXR10|ZTE\s+Corporation|ZXAN', re.I)

def is_zte_device(output: str) -> bool:
    return bool(ZTE_DEVICE_RE.search(output))
