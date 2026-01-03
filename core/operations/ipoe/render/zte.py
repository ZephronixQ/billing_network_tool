# ipoe/adapter/ZTE/render/zte.py

from core.operations.ipoe.adapter.ZTE.tables.zte_report import print_zte_report


class ZTERenderer:
    def render(self, data: dict, port: str) -> None:
        print_zte_report(
            port=port,
            device=data.get("device", {}),
            port_info=data.get("port", {}),
            traffic=data.get("traffic", {}),
            mac=data.get("mac", []),
            dhcp=data.get("dhcp", []),
            logs=data.get("logs", []),
            mac_protect=data.get("mac_protect"),
        )
