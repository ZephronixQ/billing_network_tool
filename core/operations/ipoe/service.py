from .detect_vendor import detect_vendor
from .adapter.factory import get_adapter
from core.operations.ipoe.adapter.ZTE.tables import (
    print_device_info,
    print_port_info,
)


async def run_ipoe(host: str, port: str):
    vendor = await detect_vendor(host)

    adapter = get_adapter(
        vendor=vendor,
        host=host,
        port=port,
    )

    result = await adapter.run()
    if not result:
        return

    # ✅ ВОТ ЧЕГО НЕ ХВАТАЛО
    print_device_info(result["device"])
    print_port_info(port, result["port"])
