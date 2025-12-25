import asyncio
from config.secrets import SWITCHES
from output.table import print_uncfg_table
from core.operations.onu.vendors.zte.c320.v_current.adapter import ZTEC320Adapter

SEM = asyncio.Semaphore(len(SWITCHES))
adapter = ZTEC320Adapter()

async def fetch_uncfg(host):
    async with SEM:
        try:
            onus = await adapter.fetch_uncfg(host)
            return {"host": host, "onus": onus} if onus else None
        except Exception:
            return None

async def run_uncfg():
    tasks = [fetch_uncfg(sw) for sw in SWITCHES]
    results = [r for r in await asyncio.gather(*tasks) if r]
    print_uncfg_table(results)
