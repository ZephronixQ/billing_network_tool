from .parsers.eltex_ipoe_device import parse_device
from .parsers.eltex_ipoe_interface import parse_interface, resolve_eltex_interface
from .parsers.eltex_ipoe_mac import parse_mac_table
from .parsers.eltex_ipoe_logs import parse_logs
from . import commands as cmd

def build_query_plan(port: int):
    plan = [
        {
            "key": "device",
            "commands": [cmd.SHOW_SYSTEM_MES],
            "parser": parse_device,
        },
        {
            "key": "interface",
            "commands": lambda ctx: [
                cmd.SHOW_INTERFACE.format(
                    int_type=resolve_eltex_interface(
                        ctx["device"]["model"], port
                    )[0],
                    port=resolve_eltex_interface(
                        ctx["device"]["model"], port
                    )[1],
                )
            ],
            "parser": parse_interface,
        },
        {
            "key": "mac",
            "commands": lambda ctx: (
                [
                    cmd.SHOW_MAC_TABLE.format(
                        int_type=resolve_eltex_interface(
                            ctx["device"]["model"], port
                        )[0],
                        port=resolve_eltex_interface(
                            ctx["device"]["model"], port
                        )[1],
                    )
                ]
                if ctx["interface"].get("status") == "up"
                else None
            ),
            "parser": parse_mac_table,
        },
        {
            "key": "logs",
            "commands": lambda ctx: [
                cmd.SHOW_LOGGING_INCLUDE.format(
                    short_port=(
                        f"{resolve_eltex_interface(ctx['device']['model'], port)[0][:2].lower()}"
                        f"{resolve_eltex_interface(ctx['device']['model'], port)[1]}"
                    )
                )
            ],
            "parser": lambda raw, ctx: parse_logs(
                raw,
                f"{resolve_eltex_interface(ctx['device']['model'], port)[0][:2].lower()}"
                f"{resolve_eltex_interface(ctx['device']['model'], port)[1]}",
            ),
        },
    ]

    return plan
