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
    parser.add_argument("--disable", action="store_true", help="Disable port")
    parser.add_argument("--enable", action="store_true", help="Enable port")
    parser.add_argument("--restart", action="store_true", help="Restart port")

    parser.add_argument(
        "--speed",
        metavar="MODE",
        help=(
            "Set IPOE port speed\n"
            "ZTE: 10 | 100\n"
            "SNR: auto, force10-full, force10-half, "
            "force100-full, force100-fx, force100-half, "
            "force1g-full, force1g-half, force10g-full"
        )
    )

    # ───── GPON REMOVE ONU ─────
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove ONU from OLT (GPON)"
    )

    # ───── IPOE MASS STATUS CHECK ─────
    parser.add_argument(
        "--ipoe-info-status",
        action="store_true",
        help="Run IPOE status check for multiple IPs from file"
    )

    parser.add_argument("--patch", metavar="FILE")

    # ───── GPON MASS STATUS ─────
    parser.add_argument(
        "--gpon-info-status",
        action="store_true",
        help="Run GPON ONU status check for multiple OLTs"
    )

    # ───── GPON INTERFACE CONF ─────
    parser.add_argument(
        "--gpon-conf",
        action="store_true",
        help="Special interface control for master (enable/disable whole interface)"
    )

    parser.add_argument(
        "--user",
        metavar="USERNAME",
        help="Encrypted username for special interface control"
    )

    parser.add_argument(
        "--olt",
        metavar="OLT_IP",
        help="Target OLT IP for interface control"
    )

    parser.add_argument(
        "--interface",
        metavar="INTERFACE",
        help="Target interface, e.g., 1/1/10"
    )

    return parser.parse_args()
