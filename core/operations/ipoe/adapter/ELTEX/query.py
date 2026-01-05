from . import commands as cmd

from .parsers.eltex_ipoe_device import parse_device
from .parsers.eltex_ipoe_interface import (
    determine_interface_type,
    parse_interface,
)
from .parsers.eltex_ipoe_mac import parse_mac_table
from .parsers.eltex_ipoe_logs import parse_logs


def build_query_plan(port: str):
    cli_port = f"1/0/{port}"

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
                    int_type=determine_interface_type(ctx["device"]["speed"]),
                    port=cli_port,
                )
            ],
            "parser": parse_interface,
        },
        {
            "key": "mac",
            "commands": lambda ctx: (
                [
                    cmd.SHOW_MAC_TABLE.format(
                        int_type=determine_interface_type(ctx["device"]["speed"]),
                        port=cli_port,
                    )
                ]
                if ctx["interface"].get("status") == "up"
                else []
            ),
            "parser": parse_mac_table,
        },
        {
            "key": "logs",
            "commands": lambda ctx: [
                cmd.SHOW_LOGGING_INCLUDE.format(
                    short_port=(
                        f"{determine_interface_type(ctx['device']['speed'])[:2].lower()}"
                        f"{cli_port}"
                    )
                )
            ],
            "parser": lambda raw, ctx=None: parse_logs(
                raw,
                f"{determine_interface_type(ctx['device']['speed'])[:2].lower()}{cli_port}",
            ),
        },
    ]

    return plan
