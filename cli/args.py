import argparse


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "--help",
        action="store_true",
        help="Show help"
    )

    parser.add_argument(
        "--uncfg",
        action="store_true",
        help="Show unregistered ONU on all OLTs"
    )

    parser.add_argument(
        "--gpon",
        metavar="SERIAL",
        help="Search ONU by GPON serial number"
    )

    parser.add_argument(
        "--ipoe",
        nargs=2,
        metavar=("IP", "PORT"),
        help="Run IPOE diagnostics or control port"
    )

    # ───── IPOE CONTROL FLAGS ─────
    parser.add_argument(
        "--disable",
        action="store_true",
        help="Disable IPOE port"
    )

    parser.add_argument(
        "--enable",
        action="store_true",
        help="Enable IPOE port"
    )

    parser.add_argument(
        "--restart",
        action="store_true",
        help="Restart IPOE port"
    )

    parser.add_argument(
        "--speed",
        type=int,
        choices=[10, 100],
        help="Set IPOE port speed (10 or 100)"
    )

    return parser.parse_args()
