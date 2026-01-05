import asyncio
import telnetlib3
import re

# ============================================================
# INPUT
# ============================================================
def get_user_input():
    host = "172.31.6.240"
    password = "asdzx1390"
    port = "13"  # порт из биллинга
    return host, password, port


# ============================================================
# DEVICE CONSTANTS (FAST LOOKUP)
# ============================================================
DEVICE_MODEL_DB = {
    "MES2348B":   {"vendor": "ELTEX", "ge": 48, "sfp": 4},
    "MES1124MB":  {"vendor": "ELTEX", "fe": 24, "ge": 4},
}

MODEL_RE = re.compile(r"\b(MES\d+[A-Z]+)\b")


# ============================================================
# TELNET CORE
# ============================================================
PROMPT_RE = re.compile(r"\n?\S+#\s*$")


async def read_until_prompt(reader, timeout=3.0):
    buf = ""
    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
            if not chunk:
                break
            buf += chunk
            if PROMPT_RE.search(buf):
                break
        except asyncio.TimeoutError:
            break
    return buf


async def send_command(reader, writer, command, timeout=3.0):
    writer.write(command + "\n")
    output = ""

    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(4096), timeout)
            if not chunk:
                break

            output += chunk

            if "---- More ----" in chunk or "More:" in chunk:
                writer.write(" ")
                continue

            if PROMPT_RE.search(output):
                break

        except asyncio.TimeoutError:
            break

    return output


async def telnet_login(host, password):
    reader, writer = await telnetlib3.open_connection(host=host, port=23)

    writer.write("admin\n")
    await asyncio.sleep(0.2)
    writer.write(password + "\n")
    await asyncio.sleep(0.4)

    await read_until_prompt(reader)

    writer.write("terminal length 0\n")
    await asyncio.sleep(0.2)
    await read_until_prompt(reader)

    return reader, writer


# ============================================================
# FAST DEVICE DETECT
# ============================================================
def fast_detect_device(output: str):
    m = MODEL_RE.search(output)
    if not m:
        return {
            "model": "UNKNOWN",
            "vendor": "UNKNOWN",
            "ports": "Unknown",
            "speed": "Unknown",
            "ports_detail": {},
        }

    model = m.group(1)
    info = DEVICE_MODEL_DB.get(model)

    if not info:
        return {
            "model": model,
            "vendor": "UNKNOWN",
            "ports": "Unknown",
            "speed": "Unknown",
            "ports_detail": {},
        }

    total_ports = sum(
        v for k, v in info.items() if k in ("fe", "ge", "sfp")
    )

    speed = "1G/10G" if info.get("sfp") else "100M/1G"

    return {
        "model": model,
        "vendor": info["vendor"],
        "ports": total_ports,
        "speed": speed,
        "ports_detail": info,
    }


# ============================================================
# PARSERS
# ============================================================
def determine_interface_type(speed: str):
    if speed.startswith("1G"):
        return "GigabitEthernet"
    return "FastEthernet"


def parse_interface(output: str):
    status_match = re.search(r"is (\w+) \(connected\)", output)
    status = status_match.group(1).lower() if status_match else "down"

    if status != "up":
        return {"status": "down"}

    duplex_speed_match = re.search(
        r"Full-duplex,\s+(\d+Mbps),.*media type is (\S+)", output
    )

    input_match = re.search(r"15 second input rate is (\d+) Kbit/s", output)
    output_match = re.search(r"15 second output rate is (\d+) Kbit/s", output)

    input_errors_match = re.search(r"(\d+) input errors", output)
    output_errors_match = re.search(r"(\d+) output errors", output)

    return {
        "status": "up",
        "link_speed": duplex_speed_match.group(1) if duplex_speed_match else "Unknown",
        "media_type": duplex_speed_match.group(2) if duplex_speed_match else "Unknown",
        "input_rate": input_match.group(1) if input_match else "0",
        "output_rate": output_match.group(1) if output_match else "0",
        "input_errors": input_errors_match.group(1) if input_errors_match else "0",
        "output_errors": output_errors_match.group(1) if output_errors_match else "0",
    }


def parse_mac_table(output: str):
    entries = []
    for line in output.splitlines():
        match = re.match(
            r"^(\d+)\s+([0-9a-f:]{17})\s+\S+\s+(\S+)",
            line.strip(),
            re.I,
        )
        if match:
            vlan, mac, type_ = match.groups()
            entries.append({"vlan": vlan, "mac": mac, "type": type_})
    return entries


def parse_logs(output: str, short_port: str, max_lines=15):
    lines = []
    port_re = re.compile(rf"\b{re.escape(short_port)}\b", re.I)
    prompt_re = re.compile(r"^\S+#\s*$")

    for raw in output.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("show logging"):
            continue
        if prompt_re.match(line):
            continue
        if line.startswith("More:"):
            continue
        if port_re.search(line):
            lines.append(line)
        if len(lines) >= max_lines:
            break

    return lines


# ============================================================
# MAIN
# ============================================================
async def main():
    host, password, port = get_user_input()

    # <<< ЕДИНСТВЕННОЕ ПРЕОБРАЗОВАНИЕ ПОРТА >>>
    cli_port = f"1/0/{port}"

    reader, writer = await telnet_login(host, password)

    detect_out = await send_command(
        reader, writer,
        "show system | include MES"
    )

    device = fast_detect_device(detect_out)

    print("\n===== SWITCH DATA =====")
    print(f"✔ Vendor: {device['vendor']}")
    print(f"✔ Model: {device['model']}")
    print(f"✔ Ports: {device['ports']}")
    print(f"✔ Speed: {device['speed']}")

    int_type = determine_interface_type(device["speed"])
    short_port = f"{int_type[:2].lower()}{cli_port}"

    int_out = await send_command(
        reader, writer,
        f"show interfaces {int_type} {cli_port}"
    )

    port_info = parse_interface(int_out)

    print("\n===== PORT STATE =====")
    print(f"Порт {cli_port}: {port_info['status'].upper()}")

    if port_info["status"] == "up":
        print("\n===== LINK =====")
        print(f"Speed: {port_info['link_speed']}")
        print(f"Media: {port_info['media_type']}")

        print("\n===== TRAFFIC =====")
        print(f"Input: {port_info['input_rate']} Kbit/s")
        print(f"Output: {port_info['output_rate']} Kbit/s")

        print("\n===== ERRORS =====")
        print(f"Input errors: {port_info['input_errors']}")
        print(f"Output errors: {port_info['output_errors']}")

        mac_out = await send_command(
            reader, writer,
            f"show mac address-table interface {int_type} {cli_port}"
        )

        macs = parse_mac_table(mac_out)

        if macs:
            print("\n===== MAC TABLE =====")
            for m in macs:
                print(f"MAC: {m['mac']} VLAN: {m['vlan']} TYPE: {m['type']}")
        else:
            print("\n⚠ MAC не найдены")

    log_out = await send_command(
        reader, writer,
        f"show logging | include {short_port}"
    )

    logs = parse_logs(log_out, short_port)

    print("\n===== LOGS =====")
    if logs:
        for l in logs:
            print(l)
    else:
        print("⚠ Логи не найдены")

    writer.close()


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    asyncio.run(main())
