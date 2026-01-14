from output.table_base import render_table
from output.colors import GREEN, RED, CYAN, MAGENTA, YELLOW, BLUE, RESET

DOWN_RX_WARN_THRESHOLD = 27.0  # dBm

def print_pon_power_table(rows, detail_logs=None):
    table_rows = []
    no_signal_detected = False
    low_signal_warnings = []

    headers = [
        f"{BLUE}DIR{RESET}",
        f"{BLUE}OLT{RESET}",
        f"{BLUE}ONU{RESET}",
        f"{BLUE}ATTENUATION{RESET}",
    ]

    # Таблица всегда строится
    if not rows:
        rows = []

    for r in rows:
        direction = r.get("direction", "-")
        olt = r.get("olt") or "не определён"
        onu = r.get("onu") or "не определён"
        attenuation = r.get("attenuation") or "не определено"
        onu_rx = r.get("onu_rx")

        table_rows.append([
            f"{GREEN if direction.upper() == 'UP' else RED}{direction}{RESET}",
            f"{CYAN}{olt}{RESET}",
            f"{MAGENTA}{onu}{RESET}",
            f"{YELLOW}{attenuation}{RESET}",
        ])

        # Downstream анализ
        if direction.upper() == "DOWN":
            if onu_rx in (None, "-", ""):
                no_signal_detected = True
            elif isinstance(onu_rx, (int, float)) and onu_rx > DOWN_RX_WARN_THRESHOLD:
                low_signal_warnings.append(onu_rx)

    # --- Вывод таблицы ---
    if not table_rows:
        table_rows = [["-", "не определён", "не определён", "не определено"]]

    render_table(
        rows=table_rows,
        headers=headers,
        title=f"\n{CYAN}📡 PON POWER LEVELS{RESET}",
    )

    # --- Проверка событий по последнему логу ---
    if detail_logs:
        last_log = detail_logs[-1]
        last_cause = last_log.get("cause", "").lower()
        offline_time = last_log.get("offline_time", "")

        if last_cause == "dyinggasp" and offline_time != "0000-00-00 00:00:00":
            print(f"{RED}⚠ Зафиксировано корректное отключение ONU (DyingGasp){RESET}")
            print(" - Абонент выключил питание ONU")
            print(" - Возможен выход ONU из строя (сгорание)")
            return

        if last_cause == "shutdown":
            print(f"{RED}⚠ ONU выключена вручную (Shutdown){RESET}")
            print(" - Абонент/администратор выключил ONU")
            return

        if last_cause == "los":
            print(f"{RED}❗ Оптический сигнал ONU отсутствует (L1){RESET}")
            print(" - Возможен обрыв оптического волокна")
            return
        
        if last_cause == "losi":
            print(f"{RED}❗ Оптический сигнал ONU отсутствует (L1){RESET}")
            print(" - Требуется проверка на стороне абонента")
            return

    # --- Диагностика отсутствия Rx (если логов нет) ---
    if no_signal_detected:
        print(f"{RED}❗ Оптический сигнал ONU отсутствует{RESET}")
        print(" - Требуется проверка на стороне абонента")

    # --- Низкий уровень Rx ---
    for rx in low_signal_warnings:
        print(f"{RED}ВНИМАНИЕ:{RESET} низкий уровень downstream-сигнала — Rx {rx} dBm")
