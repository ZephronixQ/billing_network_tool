import re

# ---------- DEVICE MODEL DB ----------

DEVICE_MODEL_DB = {
    "DGS-1100-10/ME": {
        "vendor": "DLINK",
        "ge": 8,
        "sfp": 2,
    },
    "DES-1210-28/ME": {
        "vendor": "DLINK",
        "fe": 24,
        "ge": 4,
    },
}

# ---------- REGEX ----------

MODEL_RE = re.compile(r'Device Type\s*:\s*([^\s]+)')

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clean_line(line: str) -> str:
    line = ansi_escape.sub("", line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()