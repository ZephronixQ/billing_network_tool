from core.connection.telnet import send_ipoe

async def detect_vendor(reader, writer) -> str:
    outputs = []

    outputs.append(await send_ipoe(reader, writer, ["show version"]))
    outputs.append(await send_ipoe(reader, writer, ["show system"]))
    outputs.append(await send_ipoe(reader, writer, ["show switch"]))

    text = "\n".join(outputs).lower()

    if "zte corporation" in text or "zxr10" in text:
        return "ZTE"

    # if "snr" in text or "foxgate" in text:
    #     return "SNR"

    return "UNKNOWN"
