from core.operations.ipoe.adapter.ZTE.tables.zte_device import print_device_info
from core.operations.ipoe.adapter.ZTE.tables.zte_port_status import print_port_status
from core.operations.ipoe.adapter.ZTE.tables.zte_mac import print_mac_table
from core.operations.ipoe.adapter.ZTE.tables.zte_dhcp import print_dhcp
from core.operations.ipoe.adapter.ZTE.tables.zte_logs import print_logs
from core.operations.ipoe.adapter.ZTE.tables.zte_mac_protect import print_mac_protect

def print_zte_report(
    *,
    port: str,
    device: dict,
    port_info: dict,
    traffic: dict,
    mac: list,
    dhcp: list,
    logs: list,
    mac_protect: dict | None,
) -> None:
    print_device_info(device)
    print_port_status(
        port=port,
        info=port_info,
        traffic=traffic,
    )

    if port_info.get("state") != "UP":
        print_logs(logs)
        return

    print_mac_protect(mac_protect)

    # ==== Исправленный блок для отображения всех MAC на порту ====
    mac_entries = [m for m in mac if m["port"] == port]

    if not mac_entries:
        print_mac_table(None)

    elif len(mac_entries) == 1:
        print_mac_table(mac_entries[0])

    else:
        print_mac_table(mac_entries)
    # =============================================================

    # DHCP — привязываем только если MAC один
    dhcp_entry = None
    if len(mac_entries) == 1:
        dhcp_entry = next(
            (d for d in dhcp if d["mac_plain"] == mac_entries[0]["mac_plain"]),
            None,
        )

    print_dhcp(dhcp_entry)
    print_logs(logs)
