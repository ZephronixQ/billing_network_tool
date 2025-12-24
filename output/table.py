from collections import defaultdict
from tabulate import tabulate
from output.colors import GREEN, YELLOW, CYAN, BLUE, RESET

def print_uncfg_table(results):
    if not results:
        print("✅ No unregistered ONU found")
        return
    grouped = defaultdict(lambda: defaultdict(list))

    # Группируем по IP и порту
    for res in results:
        ip = res["host"]
        for onu in res["onus"]:
            grouped[ip][onu["port"]].append(onu["serial"])

    rows = []
    for ip in sorted(grouped.keys(), key=lambda x: tuple(map(int, x.split(".")))):
        for port in sorted(grouped[ip].keys(), key=lambda x: tuple(map(int, x.split("/")))):
            serials = ", ".join(grouped[ip][port])
            rows.append([ip, port, serials, len(grouped[ip][port])])

    # Общий счётчик
    total_uncfg = sum(r[3] for r in rows)
    print(f"📊 Total unregistered ONU: {CYAN}{total_uncfg}{RESET}")

    # Подготовка строк с цветами
    colored_rows = [
        [
            f"{GREEN}{r[0]}{RESET}",
            f"{YELLOW}{r[1]}{RESET}",
            f"{CYAN}{r[2]}{RESET}",
            f"{CYAN}{r[3]}{RESET}"
        ]
        for r in rows
    ]

    # Таблица
    print(tabulate(
        colored_rows,
        headers=[f"{BLUE}IP{RESET}", f"{BLUE}PORT{RESET}", f"{BLUE}SERIALS{RESET}", f"{BLUE}COUNT{RESET}"],
        tablefmt="fancy_grid",
        stralign="center"
    ))

    # 📌 Сводка по каждому коммутатору
    print("\n📌 Summary per switch:")
    for ip in sorted(grouped.keys(), key=lambda x: tuple(map(int, x.split(".")))):
        switch_total = sum(len(v) for v in grouped[ip].values())
        print(f"{GREEN}{ip}{RESET} -> Total unregistered ONU: {CYAN}{switch_total}{RESET}")