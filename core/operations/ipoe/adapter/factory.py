# core/operations/ipoe/adapter/factory.py

from core.operations.ipoe.common.exceptions import UnsupportedVendor

# from core.operations.ipoe.adapter.snr.adapter import SNRIPOEAdapter
from core.operations.ipoe.adapter.ZTE.adapter import ZTEIPoeAdapter
# from core.operations.ipoe.adapter.dlink.adapter import DLinkIPOEAdapter
# from core.operations.ipoe.adapter.eltex.adapter import EltexIPOEAdapter

# VENDOR_ADAPTERS = {
#     "ZTE": ZTEIPoEAdapter,
#     # "SNR": SNRIPOEAdapter,
#     # "ELTEX": EltexIPOEAdapter,
#     # "D-LINK": DLinkIPOEAdapter,
# }


def get_adapter(vendor: str, host: str, port: str):
    vendor = vendor.upper()

    if vendor == "ZTE":
        return ZTEIPoeAdapter(host, port)

    raise ValueError(f"Unsupported IPOE vendor: {vendor}")
