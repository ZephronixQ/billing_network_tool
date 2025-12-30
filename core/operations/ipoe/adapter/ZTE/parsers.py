import re


def extract(pattern: str, text: str, default="N/A"):
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else default


# import re


def parse_device_info(output: str) -> dict:
    model = "N/A"
    ports = "N/A"
    speed = "N/A"

    m = re.search(r'ZXR10\s+(\S+)', output)
    if m:
        model = m.group(1)

    m = re.search(
        r'Module\s+0:.*?fasteth:\s*(\d+).*?gbit:\s*(\d+)',
        output,
        re.S,
    )
    if m:
        fe = int(m.group(1))
        ge = int(m.group(2))
        ports = fe + ge
        speed = f"FastEthernet x{fe}, Gigabit x{ge}"

    return {
        "vendor": "ZTE",
        "model": model,
        "ports": ports,
        "speed": speed,
    }


import re


def parse_port_info(output: str) -> dict:
    state = "N/A"
    speed = "N/A"
    is_down = False

    # --- Link state ---
    m = re.search(r'Link\s+:\s+(up|down)', output, re.I)
    if m:
        state = m.group(1).upper()
        is_down = state == "DOWN"

    # --- Speed (ТОЛЬКО из PortStatus) ---
    m = re.search(
        r'PortStatus\s*:.*?Speed\s*:\s*([0-9A-Za-z/]+)',
        output,
        re.S | re.I,
    )
    if m:
        speed = m.group(1)

    return {
        "state": state,
        "speed": speed,
        "is_down": is_down,
    }
