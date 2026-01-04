import asyncio
import telnetlib3
import re

# ================== INPUT ==================
def get_user_input():
    host = "172.31.7.66"
    password = "asdzx1390"
    port = "1/0/3"
    return host, password, port

# ================== SUPPORTED SNR MODELS ==================
SNR_MODEL_PORTS = {
    "S2965-8T": (8, 2),
    "S2965-24T": (24, 4),
    "S2985G-48T": (48, 4),
}

# ================== FAST TELNET CORE ==================
async def read_until_prompt(reader, prompt="#", timeout=3):
    buf = ""
    end = asyncio.get_event_loop().time() + timeout

    while asyncio.get_event_loop().time() < end:
        try:
            chunk = await asyncio.wait_for(reader.read(2048), timeout=0.5)
        except asyncio.TimeoutError:
            break

        if not chunk:
            break

        buf += chunk
        if buf.rstrip().endswith(prompt):
            break

    return buf

async def send_cmd(reader, writer, cmd):
    writer.write(cmd + "\n")
    return await read_until_prompt(reader)

# ================== DEVICE INFO ==================
def parse_snr_device_model(raw: str):
    m = re.search(r"SNR-(S\d+[A-Z]*-\d+T)", raw)
    return m.group(1) if m else None

def format_ports(fe, ge):
    if fe and ge:
        return f"{fe}FE + {ge}GE ({fe + ge})"
    if ge:
        return f"{ge}GE ({ge})"
    if fe:
        return f"{fe}FE ({fe})"
    return "N/A"

# ================== FAST LOG COLLECT (OPTIMIZED) ==================
async def collect_logs(reader, writer, port, model, limit=10):
    iface = f"Ethernet{port}"
    logs = []

    # ВАЖНО: включаем пагинацию
    writer.write("terminal length 24\n")
    await read_until_prompt(reader)

    async def read_pages(max_pages=3):
        pages = 0
        buf = ""

        while pages < max_pages:
            chunk = await reader.read(4096)
            if not chunk:
                break

            if "--More--" in chunk:
                pages += 1
                writer.write(" ")
                chunk = chunk.replace("--More--", "")

            buf += chunk

            if buf.rstrip().endswith("#"):
                break

        return buf

    # ===== S2985G-48T =====
    if model == "S2985G-48T":
        writer.write("show logging flash\n")

        log_re = re.compile(
            rf"""
            ^(\d+)\s+.*?
            Line\s+protocol\s+on\s+Interface\s+{re.escape(iface)},\s+
            changed\s+state\s+to\s+(UP|DOWN)
            """,
            re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        )

        buf = ""
        max_lines = 200

        while True:
            # читаем КРУПНО
            chunk = await reader.read(16384)
            if not chunk:
                break

            buf += chunk

            # если есть pager — жмём пробел СРАЗУ
            if "--More--" in chunk:
                writer.write(" ")

            # если дошли до prompt — всё
            if chunk.rstrip().endswith("#"):
                break

            # ограничиваем объём, чтобы не раздувать память
            if buf.count("\n") > max_lines:
                break

        # ПАРСИМ ОДИН РАЗ, БЫСТРО
        for m in log_re.finditer(buf):
            logs.append(f"{m.group(1)} - {iface} - {m.group(2).upper()}")
            if len(logs) >= limit:
                break



    # ===== ALL OTHER MODELS =====
    else:
        writer.write(f"show logging | include {iface}\n")
        buf = await read_pages(max_pages=1)

        include_re = re.compile(
            rf"(\d+).*?{re.escape(iface)}.*?(UP|DOWN)",
            re.IGNORECASE,
        )

        for m in include_re.finditer(buf):
            logs.append(f"{m.group(1)} - {iface} - {m.group(2).upper()}")
            if len(logs) >= limit:
                break

    # Возвращаем обратно (если нужно дальше)
    writer.write("terminal length 0\n")
    await read_until_prompt(reader)

    return logs

# ================== TELNET COLLECT ==================
async def snr_telnet_collect(host, password, port):
    reader, writer = await telnetlib3.open_connection(
        host=host,
        port=23,
        connect_minwait=0.1,
        connect_maxwait=1,
    )

    writer.write("admin\n")
    writer.write(password + "\n")
    await read_until_prompt(reader)

    await send_cmd(reader, writer, "terminal length 0")

    raw_version = await send_cmd(reader, writer, "show version")
    model = parse_snr_device_model(raw_version)

    if model not in SNR_MODEL_PORTS:
        writer.close()
        return {"unsupported": True, "model": model}

    raw_iface = await send_cmd(
        reader, writer, f"show interface ethernet {port}"
    )
    raw_mac = await send_cmd(
        reader, writer,
        f"show mac-address-table interface ethernet {port}"
    )

    logs = await collect_logs(reader, writer, port, model)

    writer.close()

    return {
        "unsupported": False,
        "model": model,
        "iface": raw_iface,
        "mac": raw_mac,
        "logs": logs,
    }

# ================== PARSERS ==================
def extract(regex, text, default="0"):
    m = re.search(regex, text, re.I)
    return m.group(1) if m else default

def parse_snr_interface(raw: str):
    data = {}

    state_match = re.search(
        r"\b(is\s+up|is\s+down|link\s+up|link\s+down)\b",
        raw,
        re.I,
    )
    data["state"] = (
        "UP" if state_match and "up" in state_match.group(1).lower() else "DOWN"
    )

    speed_match = re.search(
        r"(?:Auto-speed:.*?|Speed\s+)(\d+)\s*(G|M)?",
        raw,
        re.I,
    )

    if speed_match:
        v = speed_match.group(1)
        u = speed_match.group(2)
        data["speed"] = f"{v}{u.upper()}" if u else f"{v}M"
    else:
        data["speed"] = "N/A"

    def i(v):
        try:
            return int(v)
        except Exception:
            return 0

    def bits_to_mb(v):
        return round(i(v) / 8 / 1024 / 1024, 2)

    data["in_5m"] = bits_to_mb(extract(r"5 minute input rate\s+(\d+)", raw))
    data["out_5m"] = bits_to_mb(extract(r"5 minute output rate\s+(\d+)", raw))
    data["in_5s"] = i(extract(r"5 second input rate\s+(\d+)", raw))
    data["out_5s"] = i(extract(r"5 second output rate\s+(\d+)", raw))
    data["input_err"] = i(extract(r"(\d+)\s+input errors", raw))
    data["output_err"] = i(extract(r"(\d+)\s+output errors", raw))
    data["crc"] = i(extract(r"(\d+)\s+CRC", raw))

    return data

def parse_snr_mac(raw: str):
    mac_re = re.compile(
        r"^("
        r"[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}|"
        r"[0-9a-fA-F]{2}([-:])[0-9a-fA-F]{2}(\2[0-9a-fA-F]{2}){4}"
        r")$"
    )

    for line in raw.splitlines():
        cols = line.split()
        if len(cols) >= 2 and cols[0].isdigit() and mac_re.match(cols[1]):
            return {"vlan": cols[0], "mac": cols[1].lower()}

    return None

# ================== OUTPUT ==================
def print_port_report(port, model, iface, mac, logs):
    fe, ge = SNR_MODEL_PORTS.get(model, (0, 0))

    print("\n===== DEVICE INFO =====")
    print("VENDOR : SNR")
    print(f"MODEL  : {model}")
    print(f"PORTS  : {format_ports(fe, ge)}")

    print(f"\n------------ [PORT {port}] ------------")

    print("\n===== LINK =====")
    print(f"STATE : {iface['state']}")

    if iface["state"] == "DOWN":
        print("\n[L1] Нет линка. Возможна физическая проблема.")
    else:
        print(f"SPEED : {iface['speed']}")

        print("\n===== PORT TRAFFIC =====")
        print(f"IN  (5m) : {iface['in_5m']} MB/s")
        print(f"OUT (5m) : {iface['out_5m']} MB/s")
        print(f"IN  (5s) : {iface['in_5s']} bytes/s")
        print(f"OUT (5s) : {iface['out_5s']} bytes/s")

        print("\n===== PORT ERRORS =====")
        print(f"INPUT  ERR : {iface['input_err']}")
        print(f"OUTPUT ERR : {iface['output_err']}")
        print(f"CRC        : {iface['crc']}")

        print("\n===== PORT MAC/VLAN =====")
        if mac:
            print(f"MAC  : {mac['mac']}")
            print(f"VLAN : {mac['vlan']}")
        else:
            print("MAC не найден")

    print("\n===== DEVICE LOGS (MAX LINES = 200)=====")
    if logs:
        for l in logs:
            print(l)
    else:
        print("Логи не найдены")

# ================== MAIN ==================
async def main():
    host, password, port = get_user_input()

    if "/" not in port:
        port = f"1/0/{port}"

    data = await snr_telnet_collect(host, password, port)

    if data.get("unsupported"):
        print(f"\nУстройство не поддерживается: {data.get('model')}")
        return

    iface = parse_snr_interface(data["iface"])
    mac = parse_snr_mac(data["mac"])

    print_port_report(
        port,
        data["model"],
        iface,
        mac,
        data["logs"],
    )

if __name__ == "__main__":
    asyncio.run(main())
