# ipoe/adapter/ZTE/tables/zte_report.py

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

    mac_entry = next(
        (m for m in mac if m["port"] == port),
        None,
    )
    print_mac_table(mac_entry)

    dhcp_entry = (
        next(
            (
                d for d in dhcp
                if d["mac_plain"] == mac_entry["mac_plain"]
            ),
            None,
        )
        if mac_entry
        else None
    )
    print_dhcp(dhcp_entry)

    print_logs(logs)
