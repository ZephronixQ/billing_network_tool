from tabulate import tabulate
from output.colors import GREEN, BLUE, YELLOW, MAGENTA, RESET


def print_sn_table(data):
    print(f"\n{GREEN}✅ ONU FOUND{RESET}")

    headers = [
        f"{BLUE}IP{RESET}",
        f"{BLUE}PORT{RESET}",
        f"{BLUE}SERIAL{RESET}",
        f"{BLUE}ID{RESET}",
    ]

    row = [
        f"{GREEN}{data['host']}{RESET}",
        f"{YELLOW}{data['port']}{RESET}",
        f"{MAGENTA}{data['serial']}{RESET}",
        f"{YELLOW}{data['remote_id']}{RESET}" if data["remote_id"] else "-",
    ]

    print(tabulate([row], headers=headers, tablefmt="fancy_grid", stralign="center"))
