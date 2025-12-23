import re
from typing import List, Dict, Tuple
from core.regex import ANSI, UNCFG_REGEX

def clean_line(line: str) -> str:
    line = ANSI.sub('', line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def parse_uncfg_onu(output: str) -> List[Dict[str, str]]:
    result = []
    for line in output.splitlines():
        line = clean_line(line)
        if not line:
            continue
        m = UNCFG_REGEX.search(line)
        if m:
            result.append({
                "port": m.group(1),
                "serial": m.group(2)
            })
    return result


def ip_key(ip: str) -> Tuple[int, int, int, int]:
    return tuple(map(int, ip.split(".")))


def port_key(port: str) -> Tuple[int, int, int]:
    return tuple(map(int, port.split("/")))
