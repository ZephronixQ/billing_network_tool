from output.colors import BLUE, GREEN, YELLOW, RESET


def print_help():
    print(f"""
{BLUE}Billing Network Tool{RESET}

Usage:
  python3 main.py [OPTIONS]

General options:
  {GREEN}--help{RESET}                      Show this help message

ONU / GPON operations:
  {GREEN}--uncfg{RESET}                     Show unregistered ONU on all configured OLTs
  {GREEN}--gpon <SERIAL>{RESET}             Search ONU by GPON serial number

IPoE operations:
  {GREEN}--ipoe <IP> <PORT>{RESET}          Run IPoE diagnostics (show commands)

IPoE port control (SET commands):
  {YELLOW}--disable{RESET}                  Disable IPoE port
  {YELLOW}--enable{RESET}                   Enable IPoE port
  {YELLOW}--restart{RESET}                  Restart IPoE port (shutdown / no shutdown)
  {YELLOW}--speed <MODE>{RESET}             Set IPoE port speed (vendor-specific)

Speed modes:
  ZTE:
    10
    100

  SNR:
    auto
    force10-full
    force10-half
    force100-full
    force100-fx
    force100-half
    force1g-full
    force1g-half
    force10g-full

Examples:
  python3 main.py --uncfg
      Display all unregistered ONU on configured OLTs.

  python3 main.py --gpon ZTEG12345678
      Search ONU by GPON serial number.

  python3 main.py --ipoe 192.11.1.11 3
      Show IPoE diagnostics for port 3.

  python3 main.py --ipoe 192.11.1.11 3 --speed 100
      Set IPoE port 3 speed to 100 Mbps (ZTE).

  python3 main.py --ipoe 192.11.1.11 2 --speed force100-full
      Set IPoE port 2 speed to force100-full (SNR).

  python3 main.py --ipoe 192.11.1.11 3 --restart
      Restart IPoE port 3.

Notes:
  - Only one operation is executed per run.
  - SET operations (--disable / --enable / --restart / --speed)
    automatically switch device to privileged (enable) mode.
  - Speed validation is performed per vendor.
  - Vendor-specific CLI logic is fully encapsulated internally.
""")
