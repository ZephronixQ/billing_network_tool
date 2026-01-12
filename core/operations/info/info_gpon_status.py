import asyncio, re
from pathlib import Path
from io import StringIO

import tabulate, telnetlib3
from tabulate import tabulate

from config.secrets import *
from core.connection.telnet import connect

OUTPUT_FILE = Path("core/operations/info/output/gpon_status_result.txt")

MAX_ONU_PER_PORT = 128
COLUMNS = 7
PROMPT = "ZXAN#"

async def read_until_onu_number(reader, timeout=8):
    buf = ""
    found = False

    try:
        while True:
            chunk = await asyncio.wait_for(reader.read(256), timeout=timeout)
            if not chunk:
                break

            buf += chunk

            if "ONU Number:" in buf:
                found = True
                try:
                    buf += await asyncio.wait_for(reader.read(256), timeout=1)
                except asyncio.TimeoutError:
                    pass
                break

    except asyncio.TimeoutError:
        pass

    return buf if found else buf

def parse_gpon(raw):
    port_usage = {}
    onu_number = "0/0"

    for line in raw.splitlines():
        line = line.strip()

        if line.startswith("ONU Number:"):
            onu_number = line.split("ONU Number:")[-1].strip()
            continue

        m1 = re.match(r"(\d+/\d+/\d+):\d+", line)
        if m1:
            port = m1.group(1)
            port_usage[port] = port_usage.get(port, 0) + 1
            continue

        m2 = re.match(r"gpon-onu_(\d+/\d+/\d+):\d+", line)
        if m2:
            port = m2.group(1)
            port_usage[port] = port_usage.get(port, 0) + 1

    ports = sorted(
        port_usage.keys(),
        key=lambda x: [int(i) for i in x.split("/")]
    )

    return ports, onu_number, port_usage

def format_onu_table(port_usage):
    ports = sorted(port_usage.items(), key=lambda x: x[1], reverse=True)
    rows, row = [], []

    for port, used in ports:
        free = MAX_ONU_PER_PORT - used
        row.append(f"{port} [{free}]")
        if len(row) == COLUMNS:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    return tabulate(rows, tablefmt="fancy_grid", stralign="center")

def format_summary_table(interfaces, active, inactive, total, free):
    headers = ["Интерфейсы", "Активные", "Неактивные", "Всего", "Свободные порты"]
    return tabulate([[interfaces, active, inactive, total, free]],
                    headers=headers,
                    tablefmt="fancy_grid",
                    stralign="center")

async def fetch_olt(ip):
    reader, writer = await connect(ip)
    if not reader:
        return None

    writer.write("terminal length 0\n")
    await writer.drain()
    await reader.read(256)

    writer.write("show gpon onu state\n")
    await writer.drain()

    raw = await read_until_onu_number(reader)

    writer.close()
    await writer.wait_closed()

    return ip, *parse_gpon(raw)

async def main():
    results = await asyncio.gather(*(fetch_olt(ip) for ip in SWITCHES))
    buf = StringIO()

    total_ports = total_active = total_connected = total_free = 0

    for res in results:
        if not res:
            continue

        ip, ports, onu_number, port_usage = res

        nums = list(map(int, re.findall(r"\d+", onu_number)))
        active = nums[0] if len(nums) > 0 else 0
        connected = nums[1] if len(nums) > 1 else 0
        inactive = connected - active
        free = sum(MAX_ONU_PER_PORT - u for u in port_usage.values())

        buf.write(f"[*] OLT: {ip}\n")
        buf.write("\n[ ] ONU availability by ports\n")
        buf.write(format_onu_table(port_usage) + "\n\n")
        buf.write(format_summary_table(len(ports), active, inactive, connected, free) + "\n\n")

        total_ports += len(ports)
        total_active += active
        total_connected += connected
        total_free += free

    final = format_summary_table(
        total_ports,
        total_active,
        total_connected - total_active,
        total_connected,
        total_free,
    )

    buf.write("[*] Total for all OLTs\n")
    buf.write(final + "\n")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(buf.getvalue(), encoding="utf-8")

    print("\n[*] Total for all OLTs\n")
    print(final)
    print(f"\nДетальный вывод сохранён в: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
