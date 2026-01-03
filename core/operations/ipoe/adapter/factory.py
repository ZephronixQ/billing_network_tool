from core.operations.ipoe.adapter.ZTE.adapter import ZTEIPoeAdapter
from core.operations.ipoe.adapter.SNR.adapter import SNRIPoeAdapter
# from core.operations.ipoe.adapter.ELTEX.adapter import EltexIPoeAdapter
# from core.operations.ipoe.adapter.DLINK.adapter import DLinkIPoeAdapter


VENDOR_ADAPTERS = {
    "ZTE": ZTEIPoeAdapter,
    "SNR": SNRIPoeAdapter,
    # "ELTEX": EltexIPoeAdapter,
    # "D-LINK": DLinkIPoeAdapter,
}


def get_adapter(vendor: str, reader, writer):
    vendor = vendor.upper()

    if vendor not in VENDOR_ADAPTERS:
        raise ValueError(f"Unsupported IPOE vendor: {vendor}")

    return VENDOR_ADAPTERS[vendor](reader, writer)
