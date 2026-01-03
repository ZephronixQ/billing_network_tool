import re

def snr_ipoe_mac(raw: str):
    mac_re = re.compile(
        r"^("
        r"[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}|"
        r"[0-9a-fA-F]{2}([-:])[0-9a-fA-F]{2}(\2[0-9a-fA-F]{2}){4}"
        r")$"
    )

    for line in raw.splitlines():
        cols = line.split()
        if len(cols) >= 2 and cols[0].isdigit() and mac_re.match(cols[1]):
            return {
                "vlan": cols[0],
                "mac": cols[1].lower(),
            }

    return None
