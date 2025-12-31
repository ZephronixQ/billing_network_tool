import asyncio
import telnetlib3
import re


# ================== INPUT ==================
def get_credentials():
    host = '172.31.6.34'
    password = 'asdzx1390'
    port = '21'
    return host, password, port

# ================== TELNET ==================
async def telnet_connect(host, password, port=23):
    reader, writer = await telnetlib3.open_connection(
        host=host,
        port=port,
        connect_minwait=0.2,
        connect_maxwait=1.0,
    )

    writer.write("admin\n")
    await asyncio.sleep(0.2)

    writer.write(password + "\n")
    await asyncio.sleep(0.4)

    return reader, writer


PROMPT_RE = re.compile(r'\)#|\(cfg\)#|>$')


async def send_bulk(reader, writer, commands, timeout=0.5):
    output = ""

    for cmd in commands:
        writer.write(cmd + "\n")
        await writer.drain()

        try:
            while True:
                chunk = await asyncio.wait_for(reader.read(4096), timeout)
                if not chunk:
                    break

                output += chunk

                if PROMPT_RE.search(chunk):
                    break

        except asyncio.TimeoutError:
            pass

    return output


# ================== HELPERS ==================
def extract(pattern, text, default="N/A"):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default


def is_zte_device(output: str) -> bool:
    return bool(re.search(r'ZXR10|ZTE\s+Corporation|ZXAN', output, re.I))


def mac_to_plain(mac: str) -> str:
    return re.sub(r'[^0-9a-f]', '', mac.lower())


# ================== PARSERS ==================
def parse_zte_device_info(output: str):
    model = extract(r'ZXR10\s+(\S+)', output)

    MODEL_PORT_MAP = {
        "2928E": (24, 4),
        "2928": (24, 4),
        "3928": (24, 4),
        "3926": (24, 2),
    }

    fe, ge = MODEL_PORT_MAP.get(model, (None, None))

    if fe is not None:
        ports = fe + ge
        speed = f"FastEthernet x{fe}, Gigabit x{ge}"
    else:
        ports = "N/A"
        speed = "N/A"

    return {
        "vendor": "ZTE",
        "model": model,
        "ports": ports,
        "speed": speed,
    }


def parse_port_info(output: str):
    ps = re.search(
        r'PortStatus\s*:\s*(.*?)(?:\n\S|\Z)',
        output,
        re.I | re.S
    )

    if not ps:
        return {"state": "N/A", "speed": "N/A"}

    block = ps.group(1)

    state = extract(r'Link\s*:\s*(up|down)', block).upper()

    speed_match = re.search(
        r'Speed\s*:\s*(\d+)\s*(M|G)bps',
        block,
        re.I
    )

    speed = (
        f"{speed_match.group(1)}{speed_match.group(2).upper()}bps"
        if speed_match else "N/A"
    )

    return {
        "state": state,
        "speed": speed,
    }


def parse_port_utilization(raw: str):
    util = re.search(
        r'Port\s+utilization\s*:\s*'
        r'input\s*([\d.,]+)%\s*,\s*output:\s*([\d.,]+)%',
        raw,
        re.I
    )

    input_val = output_val = "0.00%"

    if util:
        input_val = f"{float(util.group(1).replace(',', '.')):.2f}%"
        output_val = f"{float(util.group(2).replace(',', '.')):.2f}%"

    return {
        "input": input_val,
        "output": output_val,
    }


def parse_zte_mac(raw: str):
    table = []

    mac_re = re.compile(
        r'(?P<mac>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}).*?'
        r'port-(?P<port>\d+).*?'
        r'(?P<time>\d+:\d+:\d+:\d+)',
        re.I
    )

    vlan_re = re.compile(
        r'(?P<mac>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+(?P<vlan>\d+)',
        re.I
    )

    for line in raw.splitlines():
        m = mac_re.search(line)
        v = vlan_re.search(line)

        if not m or not v:
            continue

        table.append({
            "mac": m.group("mac").lower(),
            "mac_plain": mac_to_plain(m.group("mac")),
            "vlan": v.group("vlan"),
            "port": m.group("port"),
            "time": m.group("time"),
        })

    return table


def parse_dhcp_relay(raw: str):
    bindings = []

    dhcp_re = re.compile(
        r'(?P<mac>(?:[0-9a-f]{2}\.){5}[0-9a-f]{2})\s+'
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+'
        r'\d+\s+'
        r'(?P<vlan>\d+)\s+'
        r'(?P<port>\d+)',
        re.I
    )

    for line in raw.splitlines():
        m = dhcp_re.search(line)
        if not m:
            continue

        bindings.append({
            "mac": m.group("mac").lower(),
            "mac_plain": mac_to_plain(m.group("mac")),
            "ip": m.group("ip"),
            "vlan": m.group("vlan"),
            "port": m.group("port"),
        })

    return bindings


def parse_port_errors(statistics: str):
    return {
        "in_err": extract(r'InMACRcvErr\s*:\s*(\d+)', statistics, '0'),
        "crc": extract(r'CrcError\s*:\s*(\d+)', statistics, '0'),
    }


def parse_mac_protect(raw: str, port: str):
    for line in raw.splitlines():
        cols = line.split()
        if len(cols) >= 4 and f"port-{port}" in cols[0]:
            return cols[2]
    return "N/A"


def parse_device_logs(raw: str, port: str, limit=15):
    pattern = re.compile(rf'Port\s*:\s*{re.escape(port)}\b', re.I)
    return [l for l in raw.splitlines() if pattern.search(l)][:limit]


# ================== MAIN ==================
async def main():
    host, password, port = get_credentials()

    reader, writer = await telnet_connect(host, password)

    version_output = await send_bulk(reader, writer, ["show version"])

    if not is_zte_device(version_output):
        print("Устройство не ZTE")
        writer.close()
        return

    port_output = await send_bulk(reader, writer, [f"show port {port}"], timeout=0.5)
    util_output = await send_bulk(reader, writer, [f"show port {port} utilization"], timeout=0.5)
    mac_output = await send_bulk(reader, writer, [f"show mac dynamic port {port}"], timeout=0.5)
    dhcp_output = await send_bulk(reader, writer, ["show dhcp relay binding"], timeout=0.5)
    stat_output = await send_bulk(reader, writer, [f"show port {port} statistics"], timeout=0.5)
    mac_protect_output = await send_bulk(reader, writer, [f"show mac protect port {port}"], timeout=0.5)
    log_output = await send_bulk(reader, writer, [f"show terminal log include Port"], timeout=0.5)

    writer.close()

    device_info = parse_zte_device_info(version_output)
    port_info = parse_port_info(port_output)
    traffic = parse_port_utilization(util_output)
    mac_table = parse_zte_mac(mac_output)
    dhcp_table = parse_dhcp_relay(dhcp_output)
    port_errors = parse_port_errors(stat_output)
    mac_protect_status = parse_mac_protect(mac_protect_output, port)
    logs = parse_device_logs(log_output, port)

# ================== OUTPUT ==================
    print("\n===== DEVICE INFO =====")
    print("Vendor :", device_info["vendor"])
    print("Model  :", device_info["model"])
    print("Ports  :", device_info["ports"])
    print("Speed  :", device_info["speed"])

    print(f"\n------------ [PORT {port}] ------------")

    print("\n===== LINK =====")
    print("STATE :", port_info["state"])
    print("SPEED :", port_info["speed"])


    # ===== ЕСЛИ ПОРТ DOWN =====
    if port_info["state"] != "UP":

        print("\n===== DEVICE LOGS =====")
        if logs:
            for log in logs:
                print("~", log)
        else:
            print("⚠ Логи для порта не найдены.")

        return


    # ===== ЕСЛИ ПОРТ UP =====
    print("\n===== DHCP =====")
    mac_entry = next((m for m in mac_table if m["port"] == port), None)

    if not mac_entry:
        print("MAC не найдена")
    else:
        dhcp_entry = next(
            (d for d in dhcp_table if d["mac_plain"] == mac_entry["mac_plain"]),
            None
        )

        if dhcp_entry:
            print("MAC :", dhcp_entry["mac"])
            print("IP  :", dhcp_entry["ip"])
            print("VLAN:", dhcp_entry["vlan"])
            print("PORT:", dhcp_entry["port"])
        else:
            print("DHCP запись не найдена")

        print("\n===== MAC TABLE =====")
        print("MAC :", mac_entry["mac"])
        print("TIME:", mac_entry["time"])


    print("\n===== PORT TRAFFIC =====")
    print(f"Input: {traffic['input']}")
    print(f"Output: {traffic['output']}")

    print("\n===== PORT ERRORS =====")
    print("InMACRcvErr:", port_errors["in_err"])
    print("CrcError:", port_errors["crc"])

    print("\n===== MAC PROTECT =====")
    print("STATUS:", mac_protect_status)

    print("\n===== DEVICE LOGS =====")
    if logs:
        for log in logs:
            print("~", log)
    else:
        print("⚠ Логи для порта не найдены.")


asyncio.run(main())
