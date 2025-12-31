from . import commands as cmd
from .parsers.zte_ipoe_device import parse_zte_device_info
from .parsers.zte_ipoe_port import (
    parse_port_info,
    parse_port_errors,
    parse_mac_protect,
)
from .parsers.zte_ipoe_utilization import parse_port_utilization
from .parsers.zte_ipoe_mac import parse_zte_mac
from .parsers.zte_ipoe_dhcp import parse_dhcp_relay
from .parsers.zte_ipoe_logs import parse_device_logs


def build_query_plan(port: str):
    """
    Описывает ЧТО и КАК мы собираем
    """
    return [
        {
            "key": "device",
            "commands": cmd.SHOW_VERSION,
            "parser": parse_zte_device_info,
        },
        {
            "key": "port",
            "commands": cmd.show_port(port),
            "parser": parse_port_info,
        },
        {
            "key": "traffic",
            "commands": cmd.show_port_util(port),
            "parser": parse_port_utilization,
        },
        {
            "key": "mac",
            "commands": cmd.show_mac(port),
            "parser": parse_zte_mac,
        },
        {
            "key": "dhcp",
            "commands": cmd.SHOW_DHCP,
            "parser": parse_dhcp_relay,
        },
        {
            "key": "errors",
            "commands": cmd.show_statistics(port),
            "parser": parse_port_errors,
        },
        {
            "key": "mac_protect",
            "commands": cmd.show_mac_protect(port),
            "parser": lambda raw: parse_mac_protect(raw, port),
        },
        {
            "key": "logs",
            "commands": cmd.SHOW_LOGS,
            "parser": lambda raw: parse_device_logs(raw, port),
        },
    ]
