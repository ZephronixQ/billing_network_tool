from core.connection.telnet import send_ipoe

async def detect_vendor(reader, writer) -> str:
    outputs: list[str] = []

    outputs.append(await send_ipoe(reader, writer, ["show version"]))
    outputs.append(await send_ipoe(reader, writer, ["show system"]))
    outputs.append(await send_ipoe(reader, writer, ["show switch"]))

    text = "\n".join(outputs).lower()

    # ---------- ZTE ----------
    if (
        "zte corporation" in text
        or "zxr10" in text
    ):
        return "ZTE"

    # ---------- SNR ----------
    if (
        "snr-" in text
        or "nag llc" in text
        or "nag.ru" in text
    ):
        return "SNR"

    # ---------- ELTEX ----------
    if (
        "eltex" in text
        or "eltex ltd" in text
        or "mes" in text
        or "esr" in text
        or "ltp" in text
    ):
        return "ELTEX"

    return "UNKNOWN"
