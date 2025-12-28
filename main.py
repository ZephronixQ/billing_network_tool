import asyncio
import logging

from cli.args import parse_args
from cli.help import print_help

from core.operations.onu.uncfg import run_uncfg
from core.operations.onu.search import run_sn_search


# ─────────────────────────────────────────────
# Глушим telnetlib3 и asyncio feed_data after feed_eof
# ─────────────────────────────────────────────

logging.getLogger("telnetlib3").setLevel(logging.CRITICAL)


def silent_asyncio_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, AssertionError):
        return  # feed_data after feed_eof — игнорируем
    loop.default_exception_handler(context)


async def main():
    args = parse_args()

    if args.help:
        print_help()
        return

    if args.sn:
        await run_sn_search(args.sn)
        return

    if args.uncfg:
        await run_uncfg()
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
