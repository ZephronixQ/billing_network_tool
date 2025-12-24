from tabulate import tabulate
from typing import List


def print_table(
    rows: List[List[str]],
    headers: List[str],
    title: str | None = None
) -> None:
    BLUE = "\033[94m"
    RESET = "\033[0m"

    if title:
        print(f"\n📊 {title}\n")

    colored_headers = [f"{BLUE}{h}{RESET}" for h in headers]

    print(tabulate(
        rows,
        headers=colored_headers,
        tablefmt="fancy_grid",
        stralign="center"
    ))