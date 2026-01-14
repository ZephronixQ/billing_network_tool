from output.colors import GREEN, RED, YELLOW, BLUE, CYAN, MAGENTA, RESET
from output.table_base import render_table

def _c(val: str, color: str) -> str:
    return f"{color}{val}{RESET}"

def print_port_status(port: str, info: dict, traffic: dict | None = None):
    state = info.get("state", "N/A")
    speed = info.get("speed", "N/A")

    state_color = GREEN if state == "UP" else RED
    
    if state != "UP":
        headers = [
            f"{BLUE}PORT{RESET}",
            f"{BLUE}STATE{RESET}",
            f"{BLUE}SPEED{RESET}",
        ]

        rows = [[
            _c(port, YELLOW),
            _c(state, state_color),
            _c(speed, MAGENTA),
        ]]

        # Добавляем возможные причины для DOWN
        down_info = [
            f"{RED}❗ Порт не подключен к сети{RESET}",
            f"{YELLOW}- Возможна проблема с кабелем{RESET}",
            f"{YELLOW}- Возможно отключение на стороне абонента{RESET}",
            f"{YELLOW}- Возможный сбой оборудования{RESET}",
        ]
        # Выводим таблицу
        render_table(
            rows,
            headers,
            title=f"\n{RED}🔌 PORT STATUS{RESET}",
        )
        print("\n".join(down_info))

    else:
        input_rate = traffic.get("input", "-") if traffic else "-"
        output_rate = traffic.get("output", "-") if traffic else "-"

        headers = [
            f"{BLUE}PORT{RESET}",
            f"{BLUE}STATE{RESET}",
            f"{BLUE}SPEED{RESET}",
            f"{BLUE}INPUT{RESET}",
            f"{BLUE}OUTPUT{RESET}",
        ]

        rows = [[
            _c(port, YELLOW),
            _c(state, state_color),
            _c(speed, MAGENTA),
            _c(input_rate, GREEN),
            _c(output_rate, CYAN),
        ]]

        render_table(
            rows,
            headers,
            title=f"\n{RED}🔌 PORT STATUS{RESET}",
        )
