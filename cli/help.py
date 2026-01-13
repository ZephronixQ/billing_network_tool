from output.colors import BLUE, GREEN, YELLOW, RESET

def print_root_help():
    print(f"""
{BLUE}Billing Network Tool{RESET}

Usage:
  python3 main.py [OPTIONS]

Available commands:
  {GREEN}--uncfg{RESET}
      Show unregistered ONU on all configured OLTs

  {GREEN}--gpon <SERIAL>{RESET}
      GPON ONU diagnostics and control by serial number

  {GREEN}--ipoe <IP> <PORT>{RESET}
      IPoE port diagnostics and control

  {GREEN}--gpon-info-status --patch <FILE>{RESET}
      Mass GPON ONU status check for multiple OLTs

  {GREEN}--ipoe-info-status --patch <FILE>{RESET}
      Mass IPoE port status check for multiple devices

Use:
  python3 main.py <command> --help
to see command-specific options
""")

def print_gpon_help():
    print(f"""
{BLUE}GPON ONU operations{RESET}

Usage:
  python3 main.py --gpon <SERIAL> [OPTIONS]

Available options:
  {YELLOW}--restart{RESET}
      Restart GPON port (shutdown / no shutdown)

  {YELLOW}--disable{RESET}
      Disable GPON port (ZTE)

  {YELLOW}--enable{RESET}
      Enable GPON port (ZTE)

Notes:
  - GPON port is resolved automatically from ONU serial number
  - Currently supported vendor: ZTE (ZXAN)

Examples:
  python3 main.py --gpon GPON11X21CA1
  python3 main.py --gpon GPON11X21CA1 --restart
""")

def print_ipoe_help():
    print(f"""
{BLUE}IPoE port operations{RESET}

Usage:
  python3 main.py --ipoe <IP> <PORT> [OPTIONS]

Available options:
  {YELLOW}--disable{RESET}
      Disable port

  {YELLOW}--enable{RESET}
      Enable port

  {YELLOW}--restart{RESET}
      Restart port (shutdown / no shutdown)

  {YELLOW}--speed <MODE>{RESET}
      Set port speed (vendor-specific)

Examples:
  python3 main.py --ipoe 192.11.6.169 20
  python3 main.py --ipoe 192.11.6.169 20 --restart
  python3 main.py --ipoe 192.11.6.169 20 --speed 100
""")

def print_gpon_info_help():
    print(f"""
{BLUE}GPON mass status check{RESET}

Usage:
  python3 main.py --gpon-info-status --patch <FILE>

Description:
  Performs GPON ONU status check for multiple OLTs.

Notes:
  - Patch file must contain OLT addresses (one per line)

Example:
  python3 main.py --gpon-info-status --patch olts.txt
""")

def print_ipoe_info_help():
    print(f"""
{BLUE}IPoE mass status check{RESET}

Usage:
  python3 main.py --ipoe-info-status --patch <FILE>

Description:
  Performs IPoE port status check for multiple devices.

Notes:
  - Patch file must contain device IP addresses (one per line)

Example:
  python3 main.py --ipoe-info-status --patch switches.txt
""")
