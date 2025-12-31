from core.operations.ipoe.control.vendors.ZTE.conf_speed_and_port import ZTEPortController


VENDOR_CONTROLLERS = {
    "ZTE": ZTEPortController,
}


def get_controller(vendor: str, reader, writer):
    vendor = vendor.upper()

    if vendor not in VENDOR_CONTROLLERS:
        raise ValueError(f"Unsupported IPOE vendor: {vendor}")

    return VENDOR_CONTROLLERS[vendor](reader, writer)
