from core.output.table_base import print_table


def print_onu_sn_table(data: dict) -> None:
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    rows = [[
        f"{GREEN}{data['host']}{RESET}",
        f"{MAGENTA}{data['serial']}{RESET}",
        data["interface"],
        f"{YELLOW}{data['remote_id']}{RESET}" if data["remote_id"] else "-"
    ]]

    print_table(
        rows=rows,
        headers=["IP", "SERIAL", "PORT", "REMOTE ID"],
        title="ONU search result"
    )
