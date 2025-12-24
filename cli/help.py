import argparse


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="billing-network-tool",
        description="OLT / ONU management utility",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Show unregistered ONU on all OLTs:
    python3 main.py --uncfg

  Find ONU by serial number:
    python3 main.py --sn ZTEG12345678

Notes:
  • Commands are mutually exclusive
  • Tool exits immediately after first match (SN search)
  • Output format is unified for all commands
"""
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--uncfg",
        action="store_true",
        help="Show unregistered ONU on all OLTs"
    )

    group.add_argument(
        "--sn",
        metavar="SERIAL",
        help="Find ONU by serial number"
    )

    return parser