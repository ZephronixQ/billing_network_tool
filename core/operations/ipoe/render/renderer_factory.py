from core.operations.ipoe.render.zte import ZTERenderer
from core.operations.ipoe.render.snr import SNRRenderer


def get_renderer(vendor: str):
    vendor = vendor.upper()

    if vendor == "ZTE":
        return ZTERenderer()

    if vendor == "SNR":
        return SNRRenderer()

    raise ValueError(f"No renderer for vendor {vendor}")
