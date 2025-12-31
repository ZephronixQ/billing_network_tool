from core.connection.telnet import connect, TelnetConnectionError
from core.operations.ipoe.detect_vendor import detect_vendor
from core.operations.ipoe.adapter.factory import get_adapter
from core.operations.ipoe.render.renderer_factory import get_renderer


async def run_ipoe(host: str, port: str):
    try:
        reader, writer = await connect(host)

    except TelnetConnectionError as e:
        print()
        print("❌ CONNECTION ERROR")
        print(str(e))
        return

    try:
        vendor = await detect_vendor(reader, writer)

        if vendor is None:
            print()
            print("⚠ UNKNOWN DEVICE")
            print("Vendor is not supported or cannot be detected")
            return

        adapter = get_adapter(vendor, reader, writer)
        renderer = get_renderer(vendor)

        data = await adapter.collect(port)
        renderer.render(data, port)

    finally:
        writer.close()
