from output.colors import BLUE, GREEN, YELLOW, RESET

def print_help():
    print(f"""
{BLUE}Billing Network Tool{RESET}

Usage:
  python3 main.py [OPTIONS]

Options:
  {GREEN}--uncfg{RESET}        Show unregistered ONU on all OLTs
  {GREEN}--sn <SERIAL>{RESET}  Search ONU by serial number
  {GREEN}--help{RESET}         Show this help message

Examples:
  python3 main.py --uncfg
      Display all unregistered ONU on configured switches.

  python3 main.py --sn ZTEG12345678
      Search for ONU with serial number ZTEG12345678 on all switches.

Notes:
  - You can only run one operation at a time (either --uncfg or --sn).
  - CLI is designed to be extensible for future operations like:
      - Port reload/shutdown
      - ONU registration/deletion
      - Diagnostics (IPoE/GPON)
      - Port utilization statistics
      - Vendor-specific commands
""")