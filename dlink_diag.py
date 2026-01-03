import asyncio, telnetlib3, re

# Убираем ANSI escape-последовательности
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clean_line(line):
    line = ansi_escape.sub('', line)
    line = re.sub(r"[^\x20-\x7E]+", " ", line)  # видимые символы ASCII
    line = re.sub(r"\s+", " ", line)  # несколько пробелов -> один
    return line.strip()

def extract_speed(port_info_line):
    match = re.search(r'\b\d+(?:M|G)\b', port_info_line)
    if match:
        return match.group(0)
    return None

async def get_telnet_output(host, password, command):
    """Общий метод для получения вывода команды по Telnet"""
    reader, writer = await telnetlib3.open_connection(host=host, port=23)

    # Вход
    writer.write("admin\n")
    await asyncio.sleep(0.5)
    writer.write(password + "\n")
    await asyncio.sleep(0.5)

    # Отправка команды
    writer.write(f"{command}\n")
    await asyncio.sleep(0.5)

    output_lines = []
    more_triggered = False

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=5.0)
            if not chunk:
                break

            lines = chunk.splitlines()
            for line in lines:
                cleaned = clean_line(line)
                if cleaned:
                    output_lines.append(cleaned)

            # Постраничный вывод
            more_markers = ["----", "Next Page", "Press any key", "SPACE", "CTRL+C"]
            if any(marker in chunk for marker in more_markers) and not more_triggered:
                writer.write("q")
                await asyncio.sleep(0.2)
                more_triggered = True

            # Промпт CLI
            if any(line.startswith("DES-") for line in lines):
                break

        except asyncio.TimeoutError:
            break

    writer.close()
    await asyncio.sleep(0.2)
    return output_lines

async def show_ports_speed(host, password, port):
    lines = await get_telnet_output(host, password, f"show ports {port}")

    # Склеиваем строки с портом
    port_data = []
    collecting = False
    for line in lines:
        if line.startswith(str(port) + " "):
            port_data.append(line)
            collecting = True
        elif collecting and line and not line.startswith("DES-"):
            port_data.append(line)
        elif collecting:
            break

    full_port_info = " ".join(port_data)
    return extract_speed(full_port_info)

async def get_port_macs(host, password, port):
    lines = await get_telnet_output(host, password, f"show fdb port {port}")

    mac_table = []
    mac_regex = re.compile(r'([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}')

    for line in lines:
        cols = line.split()
        if len(cols) < 4:
            continue
        vid_candidate = cols[0]
        mac_candidate = cols[2]

        # Проверяем, что VID число, а MAC валиден
        if vid_candidate.isdigit() and mac_regex.fullmatch(mac_candidate):
            mac_table.append({
                'vid': vid_candidate,
                'mac': mac_candidate
            })

    return mac_table

async def get_port_bytes(host, password, port):
    async def run_telnet_raw():
        reader, writer = await telnetlib3.open_connection(host=host, port=23)

        # Логин (только один раз)
        writer.write("admin\n")
        await asyncio.sleep(0.4)
        writer.write(password + "\n")
        await asyncio.sleep(0.4)

        # Команда
        writer.write(f"show packet ports {port}\n")
        await asyncio.sleep(0.3)

        # Остановка интерактивного режима
        writer.write("q")
        await asyncio.sleep(0.15)
        writer.write("\x03")  # Ctrl+C
        await asyncio.sleep(0.25)

        # Чтение
        output_chunks = []
        while True:
            try:
                chunk = await asyncio.wait_for(reader.read(4096), timeout=1.0)
                if not chunk:
                    break
                output_chunks.append(chunk)

                if any(line.startswith("DES-") for line in chunk.splitlines()):
                    break

            except asyncio.TimeoutError:
                break

        try:
            writer.close()
            await asyncio.sleep(0.05)
        except:
            pass

        return "".join(output_chunks)

    # Получаем сырой вывод
    raw = await run_telnet_raw()
    raw_lines = raw.splitlines()

    # Очищаем строки
    clean_lines = []
    for l in raw_lines:
        cl = clean_line(l)
        if cl:
            clean_lines.append(cl)

    # Ищем начало блока
    start_idx = None
    for i, l in enumerate(clean_lines):
        if l.startswith(f"Port Number : {port}"):
            start_idx = i
            break

    if start_idx is None:
        return None, None

    # Ищем конец блока
    end_idx = len(clean_lines)
    for j in range(start_idx + 1, len(clean_lines)):
        if any(clean_lines[j].startswith(x) for x in ["Unicast", "Multicast", "Broadcast", "Port Number :", "DES-"]):
            end_idx = j
            break

    block = clean_lines[start_idx:end_idx]

    rx_bytes = None
    tx_bytes = None

    for line in block:
        if "RX Bytes" in line and rx_bytes is None:
            nums = re.findall(r'\d+', line)
            if nums:
                rx_bytes = int(nums[-1])

        if "TX Bytes" in line and tx_bytes is None:
            nums = re.findall(r'\d+', line)
            if nums:
                tx_bytes = int(nums[-1])

        if rx_bytes is not None and tx_bytes is not None:
            break

    return rx_bytes, tx_bytes

async def get_port_errors(host, password, port):
    """Получение только CRC ошибок RX и TX"""
    lines = await get_telnet_output(host, password, f"show error ports {port}")

    port_data = []
    collecting = False
    for line in lines:
        if re.search(rf"\b{port}\b", line) or "RX Frames" in line or "TX Frames" in line:
            port_data.append(line)
            collecting = True
        elif collecting and line and not line.startswith("DES-"):
            port_data.append(line)
        elif collecting:
            break

    if not port_data:
        return 0, 0  # по умолчанию 0, если данных нет

    # Ищем только нужные строки с CRC Error
    rx_crc = 0
    tx_crc = 0
    for line in port_data:
        # RX Frames - CRC Error
        if line.startswith("CRC Error") and not "TX Frames" in line:
            parts = line.split()
            if parts[-1].isdigit():
                rx_crc = int(parts[-1])
        # TX Frames - CRC Error
        elif "CRC Error" in line and "TX Frames" in line:
            parts = line.split()
            if parts[-1].isdigit():
                tx_crc = int(parts[-1])

    return rx_crc, tx_crc

async def get_device_logs(host, password, port, max_logs=15):
    reader, writer = await telnetlib3.open_connection(host=host, port=23)

    # Вход
    writer.write("admin\n")
    await asyncio.sleep(0.5)
    writer.write(password + "\n")
    await asyncio.sleep(0.5)

    # Команда show log
    writer.write("show log\n")
    await asyncio.sleep(0.5)

    logs = []

    # Создаем жесткий регулярный фильтр для порта
    # Совпадение: "port 1", "Port 1", "Port Number : 1" и т.п.
    port_patterns = [
        rf"\bport\s+{port}\b",
        rf"\bPort\s+{port}\b",
        rf"\bPort Number\s*:\s*{port}\b"
    ]
    port_regex = re.compile("|".join(port_patterns), re.IGNORECASE)

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout=5.0)
            if not chunk:
                break

            lines = chunk.splitlines()
            for line in lines:
                cleaned = clean_line(line)
                if not cleaned:
                    continue

                # Пропускаем навигацию и служебные строки
                if any(x in cleaned for x in ["CTRL+C", "ESC", "Quit", "Next Page", "SPACE", "Enter"]):
                    continue

                # Жесткая фильтрация по порту
                if port_regex.search(cleaned):
                    logs.append(cleaned)

            # Проверка на постраничный вывод
            more_markers = ["----", "Next Page", "Press any key", "SPACE", "CTRL+C"]
            if any(marker in chunk for marker in more_markers):
                writer.write(" ")  # нажимаем SPACE для следующей страницы
                await asyncio.sleep(0.2)
                continue

            # Промпт CLI — конец вывода
            if any(line.startswith("DES-") for line in lines):
                break

        except asyncio.TimeoutError:
            break

    writer.close()
    await asyncio.sleep(0.2)

    # Возвращаем последние max_logs
    return logs[-max_logs:]

async def get_switch_model_serial_from_output(host, password, commands):
    # Берём вывод команды show switch
    lines = await get_telnet_output(host, password, commands["switch"])

    model = None
    serial = None

    for line in lines:
        if "Device Type" in line:
            model = line.split(":", 1)[1].strip()
        elif "System Serial Number" in line:
            serial = line.split(":", 1)[1].strip()
        if model and serial:
            break

    return model, serial

async def main():
    host = input("IP устройства: ").strip()
    password = input("Пароль: ").strip()
    port = input("Порт (например 2): ").strip()
    model, serial = await get_switch_model_serial_from_output(host, password, commands)

    # ===== BASE COMMANDS =====
    commands = {
        "version": "show version",
        "system": "show system",
        "switch": "show switch"
    }
    
    # ===== ПРОВЕРКА ВЕНДОРА =====
    if not model or "DES" not in model:
        print("\n❌ Устройство не определено как D-Link (DES). Скрипт будет завершён.")
        return
    
    # ===== DEVICE INFO =====
    print(f"\n===== DEVICE =====")
    print(f"Модель: {model}")
    print(f"Серийный номер: {serial}")

    # ===== PORT SPEED =====
    speed = await show_ports_speed(host, password, port)
    if not speed:
        print(f"\n===== PORT STATUS =====")
        print(f"❌ Порт {port} не активен (DOWN).")
        print("Проверьте кабель / питание / подключение роутера")

        # ===== DEVICE LOGS =====
        logs = await get_device_logs(host, password, port)
        print(f"\n===== DEVICE LOGS =====")
        if logs:
            for log in logs:
                print(log)
        else:
            print(f"Логи для порта {port} отсутствуют")
        return  # выходим после вывода логов для DOWN порта

    # ===== PORT UP =====
    print(f"\n===== PORT SPEED =====")
    print(f"Порт: {port}")
    print("Состояние порта: UP (включен)")
    print(f"Скорость порта: {speed}")

    # ===== PORT MAC/VLAN =====
    mac_table = await get_port_macs(host, password, port)
    print(f"\n===== PORT MAC/VLAN =====")
    if mac_table:
        for entry in mac_table:
            print(f"MAC: {entry['mac']}\nVLAN: {entry['vid']}")
    else:
        print("Нет записей MAC для порта")

    # ===== PORT TRAFFIC BYTES =====
    rx_bytes, tx_bytes = await get_port_bytes(host, password, port)
    print(f"\n===== PORT TRAFFIC BYTES (Total/5sec) =====")
    print(f"RX Bytes (5s): {rx_bytes if rx_bytes is not None else 'Не найдено'}")
    print(f"TX Bytes (5s): {tx_bytes if tx_bytes is not None else 'Не найдено'}")

    # ===== PORT ERROR CRC =====
    rx_crc, tx_crc = await get_port_errors(host, password, port)
    print(f"\n===== PORT ERROR CRC =====")
    print(f"CRC Error: {rx_crc} (RX)")
    print(f"CRC Error: {tx_crc} (TX)")

    # ===== DEVICE LOGS =====
    logs = await get_device_logs(host, password, port)
    print(f"\n===== DEVICE LOGS =====")
    if logs:
        for log in logs:
            print(log)
    else:
        print(f"Логи для порта {port} отсутствуют")

if __name__ == "__main__":
    asyncio.run(main())
