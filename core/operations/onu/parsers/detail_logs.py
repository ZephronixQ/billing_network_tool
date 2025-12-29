import re

TIME_RE = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

def parse_onu_detail_logs(output: str):
    logs = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue
        if line.startswith("ZXAN#"):
            continue
        if not line[0].isdigit():
            continue

        # в строке ДОЛЖНЫ быть 2 timestamp
        times = TIME_RE.findall(line)
        if len(times) < 2:
            continue

        # аккуратно режем по пробелам (таблица ZXAN не фиксирована)
        parts = re.split(r"\s{2,}|\t+", line)

        # parts: [#, auth_time, offline_time, cause?]
        num = parts[0]
        auth_time = times[0]
        offline_time = times[1]

        cause = ""
        if len(parts) >= 4:
            # cause — всё, что НЕ похоже на дату
            tail = parts[3].strip()
            if not TIME_RE.search(tail):
                cause = tail

        logs.append({
            "num": num,
            "auth_time": auth_time,
            "offline_time": offline_time,
            "cause": cause
        })

    return logs
