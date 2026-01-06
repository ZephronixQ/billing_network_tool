from core.operations.ipoe.control.vendors.ZTE.conf_speed_and_port import ZTEPortController
from core.operations.ipoe.control.vendors.SNR.conf_speed_and_port import SNRPortController
from core.operations.ipoe.control.vendors.ELTEX.conf_speed_and_port import ELTEXPortController

VENDOR_CONTROLLERS = {
    "ZTE": ZTEPortController,
    "SNR": SNRPortController,
    "ELTEX": ELTEXPortController,
}

def get_controller(vendor: str, reader, writer):
    vendor = vendor.upper()

    if vendor not in VENDOR_CONTROLLERS:
        raise ValueError(f"Unsupported IPOE vendor: {vendor}")

    return VENDOR_CONTROLLERS[vendor](reader, writer)
