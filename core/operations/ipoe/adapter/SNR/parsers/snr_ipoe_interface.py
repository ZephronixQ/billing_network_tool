import re

def snr_ipoe_interface(raw: str) -> dict:
    data = {}

    state_match = re.search(
        r"\b(is\s+up|is\s+down|link\s+up|link\s+down)\b",
        raw,
        re.I,
    )
    data["state"] = (
        "UP" if state_match and "up" in state_match.group(1).lower() else "DOWN"
    )

    speed_match = re.search(
        r"(?:Auto-speed:.*?|Speed\s+)(\d+)\s*(G|M)?",
        raw,
        re.I,
    )

    if speed_match:
        value = speed_match.group(1)
        unit = speed_match.group(2)
        data["speed"] = f"{value}{unit.upper()}" if unit else f"{value}M"
    else:
        data["speed"] = "N/A"

    def i(v):
        try:
            return int(v)
        except Exception:
            return 0

    def bits_to_mb(v):
        return round(i(v) / 8 / 1024 / 1024, 2)

    def extract(regex):
        m = re.search(regex, raw, re.I)
        return m.group(1) if m else "0"

    data["in_5m"] = bits_to_mb(extract(r"5 minute input rate\s+(\d+)"))
    data["out_5m"] = bits_to_mb(extract(r"5 minute output rate\s+(\d+)"))
    data["in_5s"] = i(extract(r"5 second input rate\s+(\d+)"))
    data["out_5s"] = i(extract(r"5 second output rate\s+(\d+)"))
    data["input_err"] = i(extract(r"(\d+)\s+input errors"))
    data["output_err"] = i(extract(r"(\d+)\s+output errors"))
    data["crc"] = i(extract(r"(\d+)\s+CRC"))

    return data
