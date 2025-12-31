from core.operations.ipoe.adapter.ZTE.tables.zte_device import print_device_info
# from core.operations.ipoe.adapter.ZTE.tables.zte_port import print_port_info
from core.operations.ipoe.adapter.ZTE.tables.zte_port_status import print_port_status
from core.operations.ipoe.adapter.ZTE.tables.zte_mac import print_mac_table
from core.operations.ipoe.adapter.ZTE.tables.zte_dhcp import print_dhcp
# from core.operations.ipoe.adapter.ZTE.tables.zte_util import print_util
from core.operations.ipoe.adapter.ZTE.tables.zte_logs import print_logs
from core.operations.ipoe.adapter.ZTE.tables.zte_mac_protect import print_mac_protect

class ZTERenderer:
    def render(self, data: dict, port: str) -> None:
        print_device_info(data["device"])
        print_port_status(
            port=port,
            info=data["port"],
            traffic=data["traffic"],
        )
# print_port_info(port, data["port"])

        if data["port"]["state"] != "UP":
            print_logs(data["logs"])
            return

        print_mac_protect(data["mac_protect"])

        mac_entry = next(
            (m for m in data["mac"] if m["port"] == port),
            None
        )
        print_mac_table(mac_entry)

        dhcp_entry = (
            next(
                (d for d in data["dhcp"] if d["mac_plain"] == mac_entry["mac_plain"]),
                None
            )
            if mac_entry else None
        )
        print_dhcp(dhcp_entry)

        # print_util(data["traffic"])
        print_logs(data["logs"])
