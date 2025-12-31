from core.operations.ipoe.render.zte import ZTERenderer

def get_renderer(vendor: str):
    vendor = vendor.upper()

    if vendor == "ZTE":
        return ZTERenderer()

    raise ValueError(f"No renderer for vendor {vendor}")
