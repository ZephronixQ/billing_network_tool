import re

def parse_device_logs(raw: str, port: str, limit: int = 15) -> list[str]:
    pattern = re.compile(rf'Port\s*:\s*{re.escape(port)}\b', re.I)
    return [
        line for line in raw.splitlines()
        if pattern.search(line)
    ][:limit]
