from output.colors import GREEN, RED, CYAN, MAGENTA, BLUE, YELLOW, RESET
from output.table_base import render_table

def is_disable(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("disable", "status:disable")

def is_na(value: str) -> bool:
    # Любой вид "неопределено"
    return value in ("N/A", "-", "не определён", "status:N/A", None, "")

def print_oper_speed_table(remote_onu: dict, iface_speed: dict) -> str:
    """
    Вывод таблицы Operate/Speed/Throughput и диагностика.
    Возвращает фактический статус Operate для логики IP STATUS.
    """
    operate = remote_onu.get("operate")
    speed = remote_onu.get("speed")

    input_rate = iface_speed.get("input_mbps", 0)
    output_rate = iface_speed.get("output_mbps", 0)

    operate_disable = is_disable(operate)
    operate_na = is_na(operate)

    # --- Таблица всегда ---
    headers = [
        f"{BLUE}Operate status{RESET}",
        f"{BLUE}Speed status{RESET}",
        f"{BLUE}Input rate (Mbit/s){RESET}",
        f"{BLUE}Output rate (Mbit/s){RESET}",
    ]

    rows = [[
        f"{RED if operate_disable else (YELLOW if operate_na else GREEN)}"
        f"{operate if operate else '-'}{RESET}",
        f"{RED if is_disable(speed) else (YELLOW if is_na(speed) else GREEN)}"
        f"{speed if speed else '-'}{RESET}",
        f"{CYAN}{input_rate}{RESET}",
        f"{MAGENTA}{output_rate}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}⚡ OPERATE / SPEED / THROUGHPUT{RESET}",
    )

    # --- Диагностика по Operate ---
    if operate_na:
        print(f"{YELLOW}ℹ️ Статус интерфейса не определён{RESET}")
        print(" - Нет корректных данных по PON")
        print(" - Диагностика Ethernet невозможна без оптики")
    elif operate_disable:
        print(f"{RED}❗ Абонентское устройство отключено{RESET}")
        print(" - Роутер не подключен или отсутствует питание")
        print(" - Возможен аппаратный сбой или выход из строя")

    # --- Возвращаем статус для логики IP STATUS ---
    return operate if operate else "N/A"
