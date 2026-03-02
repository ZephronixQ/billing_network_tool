from output.colors import GREEN, RED, BLUE, RESET
from output.table_base import render_table


def print_errors(errors: dict | None):
    # Если данных нет
    if not errors:
        render_table(
            [[f"{GREEN}N/A{RESET}"]],
            [f"{BLUE}PORT ERRORS{RESET}"],
            title=f"\n{GREEN}ℹ PORT ERRORS{RESET}",
        )
        return

    in_err = int(errors.get("in_err", 0))
    crc = int(errors.get("crc", 0))

    # Ошибок нет
    if in_err == 0 and crc == 0:
        render_table(
            [[f"{GREEN}0{RESET}"]],
            [f"{BLUE}PORT ERRORS{RESET}"],
            title=f"\n{GREEN}✅ PORT ERRORS{RESET}",
        )
        return

    # Горизонтальная таблица: заголовки — имена ошибок
    headers = []
    row = []

    if in_err > 0:
        headers.append(f"{RED}InMACRcvErr{RESET}")
        row.append(f"{RED}{in_err}{RESET}")

    if crc > 0:
        headers.append(f"{RED}CrcError{RESET}")
        row.append(f"{RED}{crc}{RESET}")

    render_table(
        [row],
        headers,
        title=f"\n{RED}❌ PORT ERRORS DETECTED{RESET}",
    )