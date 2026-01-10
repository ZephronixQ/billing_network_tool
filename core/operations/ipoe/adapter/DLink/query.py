from .parsers.dlink_ipoe_device import parse_device_model
from .parsers.dlink_ipoe_port import parse_port
from .parsers.dlink_ipoe_mac import parse_port_macs
from .parsers.dlink_ipoe_traffic import parse_port_bytes
from .parsers.dlink_ipoe_errors import parse_port_errors
from .parsers.dlink_ipoe_logs import get_device_logs
from .commands import SHOW_SWITCH, DISABLE_CLIPAGING, SHOW_PORTS, SHOW_FDB_PORT, SHOW_SPEED, SHOW_ERROR

def build_query_plan(port: int):
    plan = [
        {
            "key": "device",
            "commands": [SHOW_SWITCH],
            "parser": parse_device_model,
        },
        {
            "key": "port_info",
            "commands": [DISABLE_CLIPAGING, SHOW_PORTS.format(port=port)],
            "parser": lambda raw: parse_port(raw, port),
        },
        {
            "key": "macs",
            "commands": lambda ctx: [SHOW_FDB_PORT.format(port=port)]
            if ctx["port_info"][0] == "UP"
            else None,
            "parser": parse_port_macs,
        },
        {
            "key": "traffic",
            "commands": [SHOW_SPEED.format(port=port)],
            "parser": parse_port_bytes,
        },
        {
            "key": "errors",
            "commands": [SHOW_ERROR.format(port=port)],
            "parser": parse_port_errors,
        },
        {
            "key": "logs",
            "commands": lambda ctx: (port, 15),
            "parser": lambda args, ctx: get_device_logs(ctx["reader"], ctx["writer"], *args),
            "async": True,
        },
    ]
    return plan
