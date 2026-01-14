from output.colors import CYAN, MAGENTA, YELLOW, BLUE, RED, RESET
from output.table_base import render_table

UNDEFINED = "не определён"

def normalize(value: str) -> str:
    if value in (None, "", "-", "—"):
        return UNDEFINED
    return value

def print_ip_status(ip_service: dict):
    ip = normalize(ip_service.get("ip"))
    mac = normalize(ip_service.get("mac"))
    vlan = normalize(ip_service.get("vlan"))

    all_missing = (
        ip == UNDEFINED and
        mac == UNDEFINED and
        vlan == UNDEFINED
    )

    headers = [
        f"{BLUE}IP{RESET}",
        f"{BLUE}MAC{RESET}",
        f"{BLUE}VLAN{RESET}",
    ]

    rows = [[
        f"{CYAN}{ip}{RESET}",
        f"{MAGENTA}{mac}{RESET}",
        f"{YELLOW}{vlan}{RESET}",
    ]]

    render_table(
        rows,
        headers,
        title=f"\n{CYAN}🌐 IP STATUS{RESET}",
    )

    if all_missing:
        print(f"{RED}IP-сервис не определён{RESET}")
        print(" - Устройство не получило IP-адрес от DHCP-сервера")
        print(" - Возможен сброс к заводским настройкам")
