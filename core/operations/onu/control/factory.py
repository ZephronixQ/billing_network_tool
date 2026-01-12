from core.operations.onu.control.vendors.ZTE.conf_port import ZTEPortController
from core.operations.onu.control.vendors.ZTE.olt_conf_port import ZTEInterfaceController

VENDOR_CONTROLLERS = {
    "ZTE": ZTEPortController,
    "ZTE": ZTEInterfaceController,
}

def get_controller(vendor: str, reader, writer):
    vendor = vendor.upper()

    if vendor not in VENDOR_CONTROLLERS:
        raise ValueError(f"Unsupported GPON (OLT) vendor: {vendor}")

    return VENDOR_CONTROLLERS[vendor](reader, writer)
