import re


def parse_mac_table(output: str) -> list[dict]:
    entries = []

    for line in output.splitlines():
        match = re.match(
            r"^(\d+)\s+([0-9a-f:]{17})\s+\S+\s+(\S+)",
            line.strip(),
            re.I,
        )
        if match:
            vlan, mac, type_ = match.groups()
            entries.append(
                {"vlan": vlan, "mac": mac, "type": type_}
            )

    return entries
