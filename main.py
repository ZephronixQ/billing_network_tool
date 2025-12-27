import asyncio

from cli.args import parse_args
from cli.help import print_help

from core.operations.onu.uncfg import run_uncfg
from core.operations.onu.search import run_sn_search


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
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
