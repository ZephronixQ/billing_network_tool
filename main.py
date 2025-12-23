import asyncio
import logging

from config.devices import SWITCHES
from core.collectors.uncfg_onu import collect_all_uncfg_onu
from core.output.table import print_table_with_uncfg_count


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger("telnetlib3").setLevel(logging.ERROR)


async def main():
    print("\n🔍 Searching unregistered ONU on all switches...\n")
    results = await collect_all_uncfg_onu(SWITCHES)
    print_table_with_uncfg_count(results)


if __name__ == "__main__":
    asyncio.run(main())