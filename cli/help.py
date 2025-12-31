from output.colors import BLUE, GREEN, YELLOW, RESET


def print_help():
    print(f"""
{BLUE}Billing Network Tool{RESET}

Usage:
  python3 main.py [OPTIONS]

General options:
  {GREEN}--help{RESET}                Show this help message

ONU / GPON operations:
  {GREEN}--uncfg{RESET}               Show unregistered ONU on all configured OLTs
  {GREEN}--gpon <SERIAL>{RESET}       Search ONU by GPON serial number

IPoE operations:
  {GREEN}--ipoe <IP> <PORT>{RESET}    Run IPoE diagnostics (show commands)

IPoE port control (SET commands):
  {YELLOW}--disable{RESET}             Disable IPoE port
  {YELLOW}--enable{RESET}              Enable IPoE port
  {YELLOW}--restart{RESET}             Restart IPoE port (disable + enable)
  {YELLOW}--speed 10|100{RESET}        Set IPoE port speed

Examples:
  python3 main.py --uncfg
      Display all unregistered ONU on configured OLTs.

  python3 main.py --gpon ZTEG12345678
      Search ONU by GPON serial number.

  python3 main.py --ipoe 172.31.6.47 3
      Show IPoE diagnostics for port 3.

  python3 main.py --ipoe 172.31.6.47 3 --speed 100
      Set IPoE port 3 speed to 100 Mbps.

  python3 main.py --ipoe 172.31.6.47 3 --restart
      Restart IPoE port 3.

Notes:
  - Only one operation is executed per run.
  - SET operations (--disable / --enable / --restart / --speed)
    automatically switch device to privileged (enable) mode.
  - Vendor-specific logic is handled internally.
""")
