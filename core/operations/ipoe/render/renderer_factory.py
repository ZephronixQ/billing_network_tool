from core.operations.ipoe.render.zte import ZTERenderer
from core.operations.ipoe.render.snr import SNRRenderer
from core.operations.ipoe.render.eltex import ELTEXRenderer

def get_renderer(vendor: str):
    vendor = vendor.upper()

    if vendor == "ZTE":
        return ZTERenderer()

    if vendor == "SNR":
        return SNRRenderer()

    if vendor == "ELTEX":
        return ELTEXRenderer()

    raise ValueError(f"No renderer for vendor {vendor}")
