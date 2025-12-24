import asyncio
from core.connection.telnet import connect, send
from output.table import print_uncfg_table  # будем переиспользовать, но чуть модифицируем для одной строки
from output.colors import GREEN, MAGENTA, YELLOW, RESET
from config.secrets import SWITCHES

SEM = asyncio.Semaphore(len(SWITCHES))

# ================== PARSER ==================
import re
from utils.cleaners import clean_line

GPON_SN_REGEX = re.compile(r'gpon-onu_(\d+/\d+/\d+:\d+)', re.I)
REMOTE_ID_REGEX = re.compile(r'port-location sub-option remote-id name (\S+) vport', re.I)

def parse_onu_interface(output: str):
    for line in output.splitlines():
        line = clean_line(line)
        m = GPON_SN_REGEX.search(line)
        if m:
            return m.group(1)
    return None

def parse_remote_id(output: str):
    for line in output.splitlines():
        line = clean_line(line)
        m = REMOTE_ID_REGEX.search(line)
        if m:
            return m.group(1)
    return None

# ================== TELNET SEARCH ==================
async def search_on_switch(host: str, serial: str):
    async with SEM:
        try:
            reader, writer = await connect(host)
            await send(reader, writer, "terminal length 0")
            output = await send(reader, writer, f"show gpon onu by sn {serial}")
            iface = parse_onu_interface(output)
            if iface:
                cfg_output = await send(reader, writer, f"show running-config interface gpon-onu_{iface}")
                remote_id = parse_remote_id(cfg_output)
                writer.close()
                return {
                    "host": host,
                    "port": iface,
                    "serial": serial,
                    "remote_id": remote_id
                }
            writer.close()
        except Exception:
            return None

async def run_sn_search(serial: str):
    # создаём реальные Task объекты
    tasks = [asyncio.create_task(search_on_switch(sw, serial)) for sw in SWITCHES]

    try:
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                # отменяем все остальные задачи
                for t in tasks:
                    if not t.done():
                        t.cancel()
                print_sn_table(result)
                return
        print(f"❌ ONU {serial} not found on any switch")
    except asyncio.CancelledError:
        pass  # безопасно игнорируем отменённые задачи

# ================== TABLE ==================
from tabulate import tabulate
from output.colors import BLUE

def print_sn_table(data):
    headers = [f"{BLUE}IP{RESET}", f"{BLUE}PORT{RESET}", f"{BLUE}SERIAL{RESET}", f"{BLUE}ID{RESET}"]
    row = [
        f"{GREEN}{data['host']}{RESET}",
        f"{YELLOW}{data['port']}{RESET}",
        f"{MAGENTA}{data['serial']}{RESET}",
        f"{YELLOW}{data['remote_id']}{RESET}" if data['remote_id'] else "-"
    ]
    print(tabulate([row], headers=headers, tablefmt="fancy_grid", stralign="center"))