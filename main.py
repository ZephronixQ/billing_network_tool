import asyncio
import logging

from cli.args import parse_args
from cli.help import print_help

from core.operations.onu.uncfg import run_uncfg
from core.operations.onu.search import run_sn_search
from core.operations.ipoe.service import run_ipoe


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

    if args.gpon:
        await run_sn_search(args.gpon)
        return

    if args.uncfg:
        await run_uncfg()
        return

    if args.ipoe:
        ip, port = args.ipoe

        # ───── IPOE PORT CONTROL (SET) ─────
        if args.disable or args.enable or args.restart or args.speed:
            from core.connection.telnet import connect
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

            return

        # ───── IPOE DIAGNOSTICS (SHOW) ─────
        await run_ipoe(
            host=ip,
            port=port,
        )
        return

    print_help()


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(silent_asyncio_exception_handler)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
