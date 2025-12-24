from collections import defaultdict
from typing import List, Dict

from core.utils import ip_key, port_key
from core.output.table_base import print_table


def print_uncfg_onu_table(
    results: List[Dict[str, List[Dict[str, str]]]]
) -> None:

    if not results:
        print("✅ No unregistered ONU found")
        return

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    SERIAL = "\033[95m"
    COUNT = "\033[96m"
    RESET = "\033[0m"

    grouped = defaultdict(lambda: defaultdict(list))

    for res in results:
        for onu in res["onus"]:
            grouped[res["host"]][onu["port"]].append(onu["serial"])

    rows = []
    for ip in sorted(grouped.keys(), key=ip_key):
        for port in sorted(grouped[ip], key=port_key):
            serials = ", ".join(grouped[ip][port])
            rows.append([
                f"{GREEN}{ip}{RESET}",
                f"{YELLOW}{port}{RESET}",
                f"{SERIAL}{serials}{RESET}",
                f"{COUNT}{len(grouped[ip][port])}{RESET}"
            ])

    total = sum(len(v) for g in grouped.values() for v in g.values())

    print_table(
        rows=rows,
        headers=["IP", "PORT", "SERIALS", "UNCFG ONU"],
        title=f"Total unregistered ONU: {total}"
    )

    print("\n📌 Summary per switch:")
    for ip in sorted(grouped.keys(), key=ip_key):
        count = sum(len(v) for v in grouped[ip].values())
        print(f"{ip} -> {count}")