import re

def parse_port(lines: list[str], port: int):
    speeds_found = []

    for line in lines:
        line = re.sub(r'\s+', ' ', line.strip())

        for m in re.finditer(r'\b(10M|100M|1000M|1G)\b', line):
            speeds_found.append(m.group(1))

    if not speeds_found:
        return "DOWN", None

    speed_priority = {
        "10M": 1,
        "100M": 2,
        "1000M": 3,
        "1G": 3,
    }

    best_speed = max(
        speeds_found,
        key=lambda s: speed_priority.get(s, 0),
    )

    return "UP", best_speed
