import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import platform
from collections import defaultdict
from datetime import datetime
from tqdm import tqdm
from tabulate import tabulate

# ----------------- Извлечение IP -----------------
def extract_ips(file_path: Path) -> list[str]:
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = set()

    with file_path.open(encoding="utf-8") as f:
        for line in f:
            for ip in ip_pattern.findall(line):
                if all(0 <= int(o) <= 255 for o in ip.split(".")):
                    ips.add(ip)

    return list(ips)

# ----------------- Ping -----------------
def ping_ip(ip: str, timeout: int) -> tuple[str, str]:
    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), ip]

    try:
        return (ip, "UP") if subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).returncode == 0 else (ip, "DOWN")
    except Exception:
        return ip, "DOWN"

# ----------------- Helpers -----------------
def ip_key(ip: str):
    return tuple(map(int, ip.split(".")))

def generate_subnet_tables(results: list[tuple[str, str]]) -> str:
    subnets = defaultdict(list)

    for ip, status in sorted(results, key=lambda x: ip_key(x[0])):
        subnet = ".".join(ip.split(".")[:3])
        subnets[subnet].append((ip, status))

    out = []

    for subnet, items in sorted(subnets.items(), key=lambda x: ip_key(x[0] + ".0")):
        up = [ip for ip, s in items if s == "UP"]
        down = [ip for ip, s in items if s == "DOWN"]

        out.append(f"\n[*] {subnet} ({len(items)} IP: {len(up)} UP, {len(down)} DOWN)")
        rows = []
        for i in range(max(len(up), len(down))):
            rows.append([
                up[i] if i < len(up) else "",
                "UP" if i < len(up) else "",
                down[i] if i < len(down) else "",
                "DOWN" if i < len(down) else ""
            ])

        out.append(
            tabulate(
                rows,
                headers=["IP (UP)", "STATUS", "IP (DOWN)", "STATUS"],
                tablefmt="fancy_grid",
                stralign="center"
            )
        )

    return "\n".join(out)

# ----------------- PUBLIC ENTRYPOINT -----------------
def run_ipoe_info_status(
    patch: str,
    max_concurrent: int = 50,
    timeout: int = 1
) -> None:
    path = Path(patch)

    if not path.exists():
        print(f"Файл не найден: {path}")
        return

    ips = extract_ips(path)
    total = len(ips)

    print(f"\nНайдено IP: {total}\n")

    results = []

    with ThreadPoolExecutor(max_workers=max_concurrent) as pool:
        futures = [pool.submit(ping_ip, ip, timeout) for ip in ips]

        for f in tqdm(as_completed(futures), total=total, desc="Парсинг IP", ncols=100):
            results.append(f.result())

    up = sum(1 for _, s in results if s == "UP")
    down = total - up

    # ---- terminal table ----
    print()
    table = [[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), up, down, total]]
    headers = ["TIME", "AVAILABLE", "UNAVAILABLE", "TOTAL"]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid", stralign="center"))

    # ---- file output ----
    out_dir = Path("core/operations/info/output")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "ipoe_status_result.txt"
    with out_file.open("w", encoding="utf-8") as f:
        f.write(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        f.write("\n\n")
        f.write(generate_subnet_tables(results))

    print(f"\nРезультаты сохранены в: {out_file}")
