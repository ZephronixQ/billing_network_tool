import asyncio
from config.secrets import SWITCHES
from core.operations.onu.adapters.zte_zxan_olt import ZteZxanOltAdapter
from core.operations.onu.tables.search import print_sn_table
from core.operations.onu.tables.ip_status import print_ip_status

SEM = asyncio.Semaphore(len(SWITCHES))
adapter = ZteZxanOltAdapter()

async def search_on_switch(host: str, serial: str):
    async with SEM:
        try:
            return await adapter.search_by_sn(host, serial)
        except Exception:
            return None

async def run_sn_search(serial: str):
    tasks = [asyncio.create_task(search_on_switch(sw, serial)) for sw in SWITCHES]

    try:
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                for t in tasks:
                    if not t.done():
                        t.cancel()
                
                print_sn_table(result)

                if result.get("ip_service"):
                    print_ip_status(result["ip_service"])

                return
        print(f"❌ ONU {serial} not found on any switch")
    except asyncio.CancelledError:
        pass
