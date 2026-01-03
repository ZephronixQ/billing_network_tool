from . import commands as cmd
from .constants import SNR_LOG_INCLUDE_MODELS
from .parsers.snr_ipoe_interface import snr_ipoe_interface
from .parsers.snr_ipoe_mac import snr_ipoe_mac
from .parsers.snr_ipoe_logs import (
    snr_collect_logs_fast,
    snr_collect_logs_include,
)


def build_query_plan(port: str, model: str):
    plan = [
        {
            "key": "port",
            "commands": cmd.SHOW_INTERFACE.format(port=port),
            "parser": snr_ipoe_interface,
        },
        {
            "key": "mac",
            "commands": cmd.SHOW_MAC_TABLE.format(port=port),
            "parser": snr_ipoe_mac,
        },
    ]

    # logs — условный шаг
    plan.append(
        {
            "key": "logs",
            "commands": None,
            "parser": (
                snr_collect_logs_include
                if model in SNR_LOG_INCLUDE_MODELS
                else snr_collect_logs_fast
            ),
        }
    )

    return plan
