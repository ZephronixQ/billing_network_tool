from collections import defaultdict
from typing import List, Dict
from tabulate import tabulate

from core.utils import ip_key, port_key


def print_table_with_uncfg_count(
    results: List[Dict[str, List[Dict[str, str]]]]
) -> None:

    if not results:
        print("✅ No unregistered ONU found")
        return

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    SERIAL = "\033[95m"
    COUNT = "\033[96m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    grouped = defaultdict(lambda: defaultdict(list))

    # --- группировка ---
    for res in results:
        ip = res["host"]
        for onu in res["onus"]:
            grouped[ip][onu["port"]].append(onu["serial"])

    # --- таблица ---
    rows = []
    for ip in sorted(grouped.keys(), key=ip_key):
        for port in sorted(grouped[ip].keys(), key=port_key):
            serials = ", ".join(grouped[ip][port])
            rows.append([ip, port, serials, len(grouped[ip][port])])

    total_uncfg = sum(r[3] for r in rows)
    print(f"\n📊 Total unregistered ONU: {COUNT}{total_uncfg}{RESET}\n")

    colored_rows = [
        [
            f"{GREEN}{ip}{RESET}",
            f"{YELLOW}{port}{RESET}",
            f"{SERIAL}{serials}{RESET}",
            f"{COUNT}{cnt}{RESET}",
        ]
        for ip, port, serials, cnt in rows
    ]

    print(tabulate(
        colored_rows,
        headers=[
            f"{BLUE}IP{RESET}",
            f"{BLUE}PORT{RESET}",
            f"{BLUE}SERIALS{RESET}",
            f"{BLUE}UNCFG ONU{RESET}",
        ],
        tablefmt="fancy_grid",
        stralign="center"
    ))

    # --- summary per switch (ВОТ ОН) ---
    print("\n📌 Summary per switch:")
    for ip in sorted(grouped.keys(), key=ip_key):
        switch_total = sum(len(v) for v in grouped[ip].values())
        print(
            f"{GREEN}{ip}{RESET} -> "
            f"Total unregistered ONU: {COUNT}{switch_total}{RESET}"
        )
