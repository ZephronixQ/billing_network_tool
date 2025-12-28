import re

def clean_line(line: str) -> str:
    if not line:
        return ""

    # убрать ANSI
    line = re.sub(r"\x1b\[[0-9;]*m", "", line)

    # нормализовать пробелы и CR
    line = line.replace("\r", "")
    line = line.replace("\xa0", " ")

    # схлопнуть пробелы
    line = re.sub(r"\s+", " ", line)

    return line.strip()
