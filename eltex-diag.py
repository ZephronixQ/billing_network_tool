import asyncio, telnetlib3, re

# ================== INPUT ==================
def get_user_input():
    host = input("IP устройства: ").strip()
    password = input("Пароль: ").strip()
    port = input("Интерфейс (например 1/0/3): ").strip()
    return host, password, port

# ================== TELNET ==================
async def send_command(reader, writer, command, read_timeout=1.5):
    writer.write(command + "\n")
    await asyncio.sleep(0.3)
    output = ""

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=read_timeout)
            if not chunk:
                break
            output += chunk

            if "---- More ----" in chunk or "more" in chunk.lower():
                writer.write(" ")
                await asyncio.sleep(0.2)
        except asyncio.TimeoutError:
            break

    return output

async def eltex_telnet_collect(host, password):
    reader, writer = await telnetlib3.open_connection(host=host, port=23)

    # Авторизация
    for cred in ["admin", password]:
        writer.write(cred + "\n")
        await asyncio.sleep(0.5)

    commands = {
        "version": "show version",
        "system": "show system",
        "switch": "show switch"
    }

    out = {}
    for key, cmd in commands.items():
        out[key] = await send_command(reader, writer, cmd)

    writer.close()
    return out

# ================== PARSERS ==================
def parse_switch_info(output: str):
    match = re.search(r"System Description:\s+(.+)", output)
    if not match:
        return None

    desc = match.group(1).strip()
    if "MES" not in desc:
        return None

    model_match = re.search(r"(MES[0-9A-Za-z]+)", desc)
    model = model_match.group(1) if model_match else "Unknown"

    ports_match = re.search(r"(\d+)-port", desc)
    ports = ports_match.group(1) if ports_match else "Unknown"

    speed_match = re.search(r"(\d+[MG]/\d+[MG])", desc)
    speed = speed_match.group(1) if speed_match else "Unknown"

    return {
        "model": model,
        "ports": ports,
        "speed": speed,
        "description": desc
    }

def find_mes_presence(outputs: dict):
    for text in outputs.values():
        if "MES" in text:
            return True
    return False

def determine_interface_type(speed: str):
    if speed in ("100M/1G", "100M/1G "):
        return "FastEthernet"
    elif speed in ("1G/10G", "1G/10G "):
        return "GigabitEthernet"
    else:
        return "FastEthernet"

def parse_interface(output: str):
    status_match = re.search(r"is (\w+) \(connected\)", output)
    status = status_match.group(1) if status_match else "down"

    if status.lower() != "up":
        return {"status": "down"}

    duplex_speed_match = re.search(r"Full-duplex, (\d+Mbps), .*media type is (\S+)", output)
    link_speed = duplex_speed_match.group(1) if duplex_speed_match else "Unknown"
    media_type = duplex_speed_match.group(2) if duplex_speed_match else "Unknown"

    input_match = re.search(r"15 second input rate is (\d+) Kbit/s", output)
    output_match = re.search(r"15 second output rate is (\d+) Kbit/s", output)
    input_rate = input_match.group(1) if input_match else "0"
    output_rate = output_match.group(1) if output_match else "0"

    input_errors_match = re.search(r"(\d+) input errors", output)
    output_errors_match = re.search(r"(\d+) output errors", output)
    input_errors = input_errors_match.group(1) if input_errors_match else "0"
    output_errors = output_errors_match.group(1) if output_errors_match else "0"

    return {
        "status": "up",
        "link_speed": link_speed,
        "media_type": media_type,
        "input_rate": input_rate,
        "output_rate": output_rate,
        "input_errors": input_errors,
        "output_errors": output_errors
    }

def parse_mac_table(output: str):
    mac_entries = []
    lines = output.splitlines()
    for line in lines:
        line = line.strip()
        match = re.match(r"^(\d+)\s+([0-9a-f:]{17})\s+(\S+)\s+(\S+)", line, re.I)
        if match:
            vlan, mac, port, type_ = match.groups()
            mac_entries.append({
                "vlan": vlan,
                "mac": mac,
                "port": port,
                "type": type_
            })
    return mac_entries

async def get_port_logs(reader, writer, short_port, max_lines=15):
    cmd = f"show logging | include {short_port}"
    writer.write(cmd + "\n")
    await asyncio.sleep(0.5)

    output = ""
    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=1.5)
            if not chunk:
                break
            output += chunk

            if "More:" in chunk or "---- More ----" in chunk:
                writer.write(" ")
                await asyncio.sleep(0.2)

        except asyncio.TimeoutError:
            break

    lines = []
    for line in output.splitlines():
        line = line.strip()
        # точное совпадение порта с границами слова \b
        if re.search(rf"\b{re.escape(short_port)}\b", line, re.I):
            # исключаем строки с MAC-адресами
            if not re.search(r"[0-9a-f]{2}(:[0-9a-f]{2}){5}", line, re.I):
                lines.append(line)

    return lines[:max_lines]

# ================== MAIN ==================
async def main():
    host, password, port = get_user_input()

    data = await eltex_telnet_collect(host, password)
    if not find_mes_presence(data):
        print("❌ Устройство не является MES или не определено.")
        return

    sys_info = parse_switch_info(data.get("system", ""))
    if not sys_info:
        print("⚠ Не удалось извлечь данные о коммутаторе.")
        return

    print("\n===== SWITCH DATA =====")
    print(f"✔ Модель: {sys_info['model']}")
    print(f"✔ Порты: {sys_info['ports']}")
    print(f"✔ Скорость коммутатора: {sys_info['speed']}")

    int_type = determine_interface_type(sys_info['speed'])
    short_port = f"{int_type[0:2].lower()}{port}"  # fa/gi

    reader, writer = await telnetlib3.open_connection(host=host, port=23)
    for cred in ["admin", password]:
        writer.write(cred + "\n")
        await asyncio.sleep(0.5)

    # ===== Данные порта =====
    interface_cmd = f"show interfaces {int_type} {port}"
    int_output = await send_command(reader, writer, interface_cmd)
    port_info = parse_interface(int_output)

    if port_info["status"] == "down":
        print('\n[ L1 ] Возможна физическая проблема:')
        print(f"❌ Порт {port} не активен (DOWN).")
        print('Проверьте кабель / питание / подключение роутера')
        writer.close()
        return

    print("\n===== LINK =====")
    print(f"Статус: {port_info['status']}")
    print(f"Скорость линка: {port_info['link_speed']}")
    print(f"Тип медиа: {port_info['media_type']}")

    print("\n===== PORT TRAFFIC =====")
    print(f"Input rate: {port_info['input_rate']} Kbit/s")
    print(f"Output rate: {port_info['output_rate']} Kbit/s")

    print('\n===== PORT ERRORS =====')
    print(f"Input errors: {port_info['input_errors']}")
    print(f"Output errors: {port_info['output_errors']}")

    # ===== MAC-адреса =====
    await asyncio.sleep(0.5)
    mac_cmd = f"show mac address-table interface {int_type} {port}"
    mac_output = await send_command(reader, writer, mac_cmd)
    await asyncio.sleep(0.5)
    mac_entries = parse_mac_table(mac_output)
    
    if mac_entries:
        print(f"\n===== PORT MAC/VLAN =====")
        for entry in mac_entries:
            print(f"MAC: {entry['mac']}\nVLAN: {entry['vlan']}\nType: {entry['type']}")
    else:
        print(f"⚠ MAC-адреса для порта {port} не найдены.")

    # ===== Логи порта =====
    await asyncio.sleep(0.5)
    port_logs = await get_port_logs(reader, writer, short_port, max_lines=15)
    writer.close()

    if port_logs:
        print(f"\n===== DEVICE LOGS =====")
        for line in port_logs:
            print(line)
    else:
        print(f"⚠ Логи для порта {short_port} не найдены.")

# ================== RUN ==================
if __name__ == "__main__":
    asyncio.run(main())
