import asyncio
import logging

from config.devices import SWITCHES
from cli.help import build_arg_parser
from core.collectors.uncfg_onu import collect_all_uncfg_onu
from core.collectors.onu_by_sn import find_onu_by_serial
from core.output.uncfg_onu_table import print_uncfg_onu_table
from core.output.onu_sn_table import print_onu_sn_table


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger("telnetlib3").setLevel(logging.ERROR)

async def async_main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.uncfg:
        results = await collect_all_uncfg_onu(SWITCHES)
        print_uncfg_onu_table(results)

    elif args.sn:
        result = await find_onu_by_serial(SWITCHES, args.sn)
        if result:
            print_onu_sn_table(result)
        else:
            print("❌ ONU not found")

if __name__ == "__main__":
    asyncio.run(async_main())