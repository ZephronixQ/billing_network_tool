# core/operations/ipoe/detect_vendor.py

import asyncio

from core.connection.telnet import connect
from core.operations.ipoe.common.exceptions import UnsupportedVendor
from core.operations.ipoe.common.utils import send_command


VENDOR_SIGNATURES = {
    "ZTE": [
        "ZTE",
        "ZXR10",
        "ZXR10-2992E",
    ],
    "SNR": [
        "SNR-S2965",
        "SNR",
    ],
    "ELTEX": [
        "ELTEX",
        "MES1124MB",
        "MES2348",
    ],
    "D-LINK": [
        "D-LINK",
        "DES-1210",
        "DGS-1100",
    ],
}


from core.connection.telnet import connect, send_bulk
async def detect_vendor(host: str) -> str:
    reader, writer = await connect(host)

    try:
        # пробуем основные команды, которые реально существуют на L2
        out1 = await send_command(reader, writer, "show version")
        out2 = await send_command(reader, writer, "display version")

        output = out1 + out2

        upper = output.upper()

        for vendor, signs in VENDOR_SIGNATURES.items():
            for s in signs:
                if s in upper:
                    return vendor

        raise UnsupportedVendor("Vendor not detected")

    finally:
        writer.close()