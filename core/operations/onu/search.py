import asyncio
from config.secrets import SWITCHES
from core.operations.onu.vendors.zte.c320.v_current.adapter import ZTEC320Adapter
from core.operations.onu.tables.search import print_sn_table

SEM = asyncio.Semaphore(len(SWITCHES))
adapter = ZTEC320Adapter()

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
                return
        print(f"❌ ONU {serial} not found on any switch")
    except asyncio.CancelledError:
        pass
