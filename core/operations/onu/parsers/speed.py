import re
from .common import clean_line


def parse_remote_onu_interface(output: str):
    operate = speed = "-"

    for line in output.splitlines():
        line = clean_line(line)

        if line.lower().startswith("operate status"):
            operate = line.split()[-1]

        elif line.lower().startswith("speed status"):
            speed = line.split()[-1]

    return {
        "operate": operate,
        "speed": speed,
    }


def parse_interface_speed(output: str):
    input_rate_mbps = output_rate_mbps = 0.0

    for line in output.splitlines():
        line = clean_line(line)

        if line.lower().startswith("input rate"):
            m = re.search(r'input rate\s*:\s*([\d.]+)\s*bps', line, re.I)
            if m:
                input_rate_mbps = float(m.group(1)) * 8 / 1_000_000

        elif line.lower().startswith("output rate"):
            m = re.search(r'output rate\s*:\s*([\d.]+)\s*bps', line, re.I)
            if m:
                output_rate_mbps = float(m.group(1)) * 8 / 1_000_000

    return {
        "input_mbps": round(input_rate_mbps, 3),
        "output_mbps": round(output_rate_mbps, 3),
    }
