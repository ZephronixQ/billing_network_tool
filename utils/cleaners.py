import re
from utils.regex import ANSI

def clean_line(line: str) -> str:
    line = ANSI.sub('', line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()

