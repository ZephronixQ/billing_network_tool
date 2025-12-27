from collections import defaultdict
from output.colors import GREEN, YELLOW, CYAN, BLUE, RESET
from output.table_base import render_table

def print_uncfg_table(results):
    if not results:
        print("✅ No unregistered ONU found")
        return

    grouped = defaultdict(lambda: defaultdict(list))
    for res in results:
        for onu in res["onus"]:
            grouped[res["host"]][onu["port"]].append(onu["serial"])

    rows = []
    for ip in sorted(grouped):
        for port in sorted(grouped[ip]):
            serials = ", ".join(grouped[ip][port])
            rows.append([
                f"{GREEN}{ip}{RESET}",
                f"{YELLOW}{port}{RESET}",
                f"{CYAN}{serials}{RESET}",
                f"{CYAN}{len(grouped[ip][port])}{RESET}",
            ])

    total = sum(len(v) for sw in grouped.values() for v in sw.values())

    render_table(
        rows,
        headers=[
            f"{BLUE}IP{RESET}",
            f"{BLUE}PORT{RESET}",
            f"{BLUE}SERIALS{RESET}",
            f"{BLUE}COUNT{RESET}",
        ],
        title=f"📊 Total unregistered ONU: {CYAN}{total}{RESET}",
    )

    print("\n📌 Summary per switch:")
    for ip in sorted(grouped):
        count = sum(len(v) for v in grouped[ip].values())
        print(f"{GREEN}{ip}{RESET} -> Total unregistered ONU: {CYAN}{count}{RESET}")
