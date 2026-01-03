import re

def extract(pattern, text, default="N/A"):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default

def mac_to_plain(mac: str) -> str:
    return re.sub(r'[^0-9a-f]', '', mac.lower())

def normalize_port(port: str) -> str:
    return port if "/" in port else f"1/0/{port}"


@staticmethod
def parse_snr_device_model(raw: str):
    m = re.search(r"SNR-(S\d+[A-Z]*-\d+T)", raw)
    return m.group(1) if m else None