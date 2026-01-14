import asyncio
from config.secrets import SWITCHES

from core.operations.onu.adapters.zte_zxan_olt import ZteZxanOltAdapter
from core.operations.onu.tables.search import print_sn_table
from core.operations.onu.tables.ip_status import print_ip_status
from core.operations.onu.tables.pon_power import print_pon_power_table
from core.operations.onu.tables.oper_speed import print_oper_speed_table

from core.operations.onu.tables.detail_logs import print_onu_detail_logs_table
from output.colors import CYAN, RESET

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
        if not result:
            continue

        # стопаем остальные OLT
        for t in tasks:
            if t is not task:
                t.cancel()

        # ===== 1. MAIN / ID =====
        print_sn_table(result)

        # ===== 2. PON POWER =====
        pon_power = result.get("pon_power") or []
        detail_logs = result.get("detail_logs")

        # PON таблица ВСЕГДА
        print_pon_power_table(
            pon_power,
            detail_logs=detail_logs
        )

        # флаг неопределённого PON
        pon_na = False
        for row in pon_power:
            if (
                "не определ" in row.get("olt", "")
                or "не определ" in row.get("onu", "")
                or "не определ" in str(row.get("attenuation"))
            ):
                pon_na = True
                break

        if not pon_power:
            pon_na = True



        # ===== 3. OPERATE / SPEED =====
        remote_onu = result.get("remote_onu")
        iface_speed = result.get("iface_speed")

        # Если PON сигнал неопределён — не выводим OPERATE / SPEED
        if pon_na:
            operate_status = None
        elif remote_onu and iface_speed:
            # Выводим таблицу и получаем статус Operate
            operate_status = print_oper_speed_table(remote_onu, iface_speed)
        else:
            operate_status = None

        # ===== 4. IP STATUS =====
        ip_service = result.get("ip_service")

        # Выводим IP только если Operate реально активен
        if ip_service and operate_status in ("enable", "status:enable"):
            print_ip_status(ip_service)



        # ===== DETAIL LOGS =====
        if result.get("detail_logs"):
            print(f"\n{CYAN}📝 ONU DETAIL LOGS{RESET}")
            print_onu_detail_logs_table(result["detail_logs"])

        return

    print(f"\n❌ ONU {serial} not found on any switch")
