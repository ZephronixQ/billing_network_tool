from core.operations.ipoe.adapter.ELTEX.constants import (
    DEVICE_MODEL_DB,
    MODEL_RE,
    SPEED_WITH_SFP,
    SPEED_NO_SFP,
)


def parse_device(output: str) -> dict:
    m = MODEL_RE.search(output)
    if not m:
        return {
            "model": "UNKNOWN",
            "vendor": "UNKNOWN",
            "ports": "Unknown",
            "speed": "Unknown",
            "ports_detail": {},
        }

    model = m.group(1)
    info = DEVICE_MODEL_DB.get(model)

    if not info:
        return {
            "model": model,
            "vendor": "UNKNOWN",
            "ports": "Unknown",
            "speed": "Unknown",
            "ports_detail": {},
        }

    total_ports = sum(
        v for k, v in info.items() if k in ("fe", "ge", "sfp")
    )

    speed = SPEED_WITH_SFP if info.get("sfp") else SPEED_NO_SFP

    return {
        "model": model,
        "vendor": info["vendor"],
        "ports": total_ports,
        "speed": speed,
        "ports_detail": info,
    }
