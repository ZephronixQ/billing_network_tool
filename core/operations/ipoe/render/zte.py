from core.operations.ipoe.adapter.ZTE.tables.zte_report import print_zte_report


class ZTERenderer:
    def render(self, data: dict, port: str):
        print_zte_report(
            port=port,
            device=data["device"],
            port_info=data["port"],
            traffic=data["traffic"],
            mac=data.get("mac", []),
            dhcp=data.get("dhcp", []),
            logs=data.get("logs", []),
            mac_protect=data.get("mac_protect"),
            errors=data.get("errors"),
        )