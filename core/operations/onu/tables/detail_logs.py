from tabulate import tabulate
from output.colors import BLUE, CYAN, MAGENTA, YELLOW, RESET


def print_onu_detail_logs_table(logs: list):
    headers = [
        f"{BLUE}#{RESET}",
        f"{BLUE}Authpass Time{RESET}",
        f"{BLUE}Offline Time{RESET}",
        f"{BLUE}Cause{RESET}",
    ]

    rows = []
    for log in logs:
        rows.append([
            f"{MAGENTA}{log['num']}{RESET}",
            f"{CYAN}{log['auth_time']}{RESET}",
            f"{CYAN}{log['offline_time']}{RESET}",
            f"{YELLOW}{log['cause']}{RESET}",
        ])

    print(
        tabulate(
            rows,
            headers=headers,
            tablefmt="fancy_grid",
            stralign="center"
        )
    )
