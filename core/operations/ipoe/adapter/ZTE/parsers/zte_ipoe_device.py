import re

MODEL_PORT_MAP = {
    "2928E": {"fe": 24, "ge": 4},
    "2928":  {"fe": 24, "ge": 4},
    "3928":  {"fe": 24, "ge": 4},
    "3926":  {"fe": 24, "ge": 2},
}


def parse_zte_device_info(output: str) -> dict:
    model = "N/A"

    # 1️⃣ PRIORITY — Module line (most accurate)
    m = re.search(
        r'Module\s+\d+:\s+ZXR10\s+(\S+);.*?fasteth:\s*(\d+);\s*gbit:\s*(\d+)',
        output,
        re.I,
    )
    if m:
        model = m.group(1)
        fe = int(m.group(2))
        ge = int(m.group(3))

        return {
            "vendor": "ZTE",
            "model": model,
            "ports": {
                "fe": fe,
                "ge": ge,
            },
            "speed": f"FastEthernet x{fe}, Gigabit x{ge}",
        }

    # 2️⃣ FALLBACK — Version Number
    m = re.search(
        r'ZXR10\s+(\d{4}\w*)\s+Version\s+Number',
        output,
        re.I,
    )
    if m:
        model = m.group(1)
        ports = MODEL_PORT_MAP.get(model)

        if ports:
            fe = ports.get("fe", 0)
            ge = ports.get("ge", 0)

            return {
                "vendor": "ZTE",
                "model": model,
                "ports": ports,
                "speed": f"FastEthernet x{fe}, Gigabit x{ge}",
            }

    # 3️⃣ FAIL-SAFE
    return {
        "vendor": "ZTE",
        "model": "N/A",
        "ports": {},
        "speed": "N/A",
    }
