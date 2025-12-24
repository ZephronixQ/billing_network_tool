import re

# ANSI и UNCFG regex как было в оригинальном скрипте
ANSI = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
UNCFG_REGEX = re.compile(
    r'gpon-onu_(\d+/\d+/\d+):\d+\s+([A-Z0-9]{8,})\s+unknown',
    re.I
)

def clean_line(line: str) -> str:
    """Удаляем ANSI и лишние символы"""
    line = ANSI.sub('', line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()

def parse_uncfg(output: str):
    """Парсинг uncfg ONU по старому стилю, как в onu_finder.py"""
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