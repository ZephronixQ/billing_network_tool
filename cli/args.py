import argparse

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "--uncfg",
        action="store_true",
        help="Show unregistered ONU on all OLTs"
    )

    parser.add_argument(
        "--sn",
        type=str,
        help="Search ONU by serial number"
    )

    parser.add_argument(
        "--help",
        action="store_true",
        help="Show help"
    )

    return parser.parse_args()