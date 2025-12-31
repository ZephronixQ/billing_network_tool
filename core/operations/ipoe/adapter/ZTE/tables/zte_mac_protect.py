from tabulate import tabulate

from output.colors import (
    GREEN,
    BLUE,
    YELLOW,
    MAGENTA,
    CYAN,
    RED,
    RESET,
)


def print_mac_protect(data: dict):
    if not data or data.get("action") == "N/A":
        return

    status = (
        f"{GREEN}Enable{RESET}"
        if data.get("enabled")
        else f"{RED}Disable{RESET}"
    )

    is_protect = (
        f"{RED}Yes{RESET}"
        if data.get("active")
        else f"{GREEN}No{RESET}"
    )

    action = f"{YELLOW}{data.get('action', 'N/A')}{RESET}"

    table = [[status, is_protect, action]]

    headers = [
        f"{CYAN}STATUS{RESET}",
        f"{CYAN}IS-PROTECT{RESET}",
        f"{CYAN}ACTION{RESET}",
    ]

    print(f"\n{MAGENTA}🛡 MAC PROTECT{RESET}")
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="fancy_grid",
            colalign=("center", "center", "center"),
        )
    )
