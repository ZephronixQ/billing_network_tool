import asyncio
import logging

from cli.args import parse_args
from cli.help import print_help

from core.operations.onu.uncfg import run_uncfg
from core.operations.onu.search import run_sn_search, adapter, SEM, SWITCHES
from core.operations.ipoe.service import run_ipoe
from core.connection.telnet import connect
from core.operations.onu.control.vendors.ZTE.conf_port import ZTEPortController

logging.getLogger("telnetlib3").setLevel(logging.CRITICAL)


def silent_asyncio_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, AssertionError):
        return
    loop.default_exception_handler(context)


async def main():
    args = parse_args()

    if args.help:
        print_help()
        return

    # ───── IPOE MASS STATUS CHECK ─────
    if args.ipoe_info_status:
        if not args.patch:
            print("Укажи путь к файлу с IP через --patch")
            return

        from core.operations.info.info_ipoe_status import run_ipoe_info_status
        run_ipoe_info_status(patch=args.patch)
        return

    # ───── GPON MASS STATUS CHECK ─────
    if args.gpon_info_status:
        from core.operations.info.info_gpon_status import main as gpon_main
        await gpon_main()
        return

    # ───── SN SEARCH ─────
    if args.gpon and not (args.disable or args.enable or args.restart or args.remove):
        await run_sn_search(args.gpon)
        return

    # ───── ONU UNCFG ─────
    if args.uncfg:
        await run_uncfg()
        return

    # ───── IPOE PORT CONTROL / DIAGNOSTICS ─────
    if args.ipoe:
        ip, port = args.ipoe

        if args.disable or args.enable or args.restart or args.speed:
            from core.operations.ipoe.detect_vendor import detect_vendor
            from core.operations.ipoe.control.factory import get_controller

            reader, writer = await connect(ip)
            try:
                vendor = await detect_vendor(reader, writer)
                controller = get_controller(vendor, reader, writer)

                if args.disable:
                    await controller.disable_port(port)
                elif args.enable:
                    await controller.enable_port(port)
                elif args.restart:
                    await controller.restart_port(port)
                elif args.speed:
                    await controller.set_port_speed(port, args.speed)

            finally:
                writer.close()
                await writer.wait_closed()
            return

        await run_ipoe(host=ip, port=port)
        return

    # ───── GPON PORT CONTROL / REMOVE ─────
    if args.gpon and (args.disable or args.enable or args.restart or args.remove):

        # --- 1. Найти ONU на OLT ---
        result = None
        async with SEM:
            for host in SWITCHES:
                try:
                    r = await adapter.search_by_sn(host, args.gpon)
                    if r:
                        iface = r.get("interface") or r.get("port") or r.get("iface")
                        if iface:
                            result = {"host": host, "interface": iface}
                            break
                except Exception:
                    continue

        if not result:
            print(f"❌ ONU {args.gpon} not found on any switch")
            return

        host = result["host"]
        iface = result["interface"]

        # --- 2. Подключение к найденному OLT ---
        reader, writer = await connect(host)
        try:
            controller = ZTEPortController(reader, writer, host, iface)

            if args.disable:
                await controller.disable_port()

            elif args.enable:
                await controller.enable_port()

            elif args.restart:
                await controller.restart_port()

            elif args.remove:
                await controller.delete_onu()
                print(f"✅ ONU {args.gpon} successfully removed")

        finally:
            writer.close()
            await writer.wait_closed()

        return

    # ───── GPON INTERFACE CONF (MASTER) ─────
    if args.gpon_conf:
        from core.operations.onu.control.vendors.ZTE.olt_conf_port import ZTEInterfaceController

        if not all([args.user, args.olt, args.interface]):
            print("❌ Для --gpon-conf необходимо указать --user, --olt и --interface")
            return

        if not (args.disable or args.enable):
            print("❌ Для --gpon-conf можно использовать только --disable или --enable")
            return

        reader, writer = await connect(args.olt)
        try:
            controller = ZTEInterfaceController(
                reader, writer,
                host=args.olt,
                interface=args.interface,
                user_token=args.user
            )

            if args.disable:
                await controller.disable_interface()
                print(f"✅ Interface {args.interface} on {args.olt} disabled")

            elif args.enable:
                await controller.enable_interface()
                print(f"✅ Interface {args.interface} on {args.olt} enabled")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

        finally:
            writer.close()
            await writer.wait_closed()
        return

    # ───── HELP ─────
    print_help()


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(silent_asyncio_exception_handler)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
