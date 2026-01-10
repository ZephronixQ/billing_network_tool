from ..constants import MODEL_RE

def parse_device_model(lines: list[str]) -> str | None:
    for line in lines:
        m = MODEL_RE.search(line)
        if m:
            return m.group(1)

    return None
