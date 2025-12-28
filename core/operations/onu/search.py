# core/operations/onu/run/search_sn.py

import asyncio
from config.secrets import SWITCHES
from core.operations.onu.adapters.zte_zxan_olt import ZteZxanOltAdapter
from core.operations.onu.tables.search import print_sn_table
from core.operations.onu.tables.ip_status import print_ip_status
from core.operations.onu.tables.pon_power import print_pon_power_table

adapter = ZteZxanOltAdapter()
SEM = asyncio.Semaphore(len(SWITCHES))


async def search_on_switch(host: str, serial: str):
    async with SEM:
        try:
            return await adapter.search_by_sn(host, serial)
        except Exception:
            return None


async def run_sn_search(serial: str):
    tasks = [
        asyncio.create_task(search_on_switch(sw, serial))
        for sw in SWITCHES
    ]

    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            # стопаем остальные OLT
            for t in tasks:
                if t is not task:
                    t.cancel()

            # ===== 1. MAIN / ID =====
            print_sn_table(result)

            # ===== 2. IP STATUS =====
            print_ip_status(result["ip_service"])

            # ===== 3. PON POWER (ВСЕГДА ПОСЛЕДНИМ) =====
            if result.get("pon_power"):
                print_pon_power_table(result["pon_power"])

            return

    print(f"\n❌ ONU {serial} not found on any switch")
