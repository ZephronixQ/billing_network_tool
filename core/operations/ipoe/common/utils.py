import re

def extract(pattern, text, default="N/A"):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default


def mac_to_plain(mac: str) -> str:
    return re.sub(r'[^0-9a-f]', '', mac.lower())
