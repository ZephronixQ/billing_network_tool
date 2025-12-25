import re

ANSI = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

def clean_line(line: str) -> str:
    line = ANSI.sub('', line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()
