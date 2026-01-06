import re
from core.operations.ipoe.adapter.ELTEX.constants import DEVICE_MODEL_DB

def resolve_eltex_interface(model: str, port: int | str) -> tuple[str, str]:
    port = int(port)

    device = DEVICE_MODEL_DB.get(model)
    if not device:
        raise ValueError(f"Unknown device model: {model}")

    fe = device.get("fe", 0)
    ge = device.get("ge", 0)
    sfp = device.get("sfp", 0)

    # --------------------------------------------------
    # FastEthernet
    # --------------------------------------------------
    if port <= fe:
        return "FastEthernet", f"1/0/{port}"

    # --------------------------------------------------
    # GigabitEthernet
    # --------------------------------------------------
    if port <= fe + ge:
        ge_port = port - fe
        return "GigabitEthernet", f"1/0/{ge_port}"

    # --------------------------------------------------
    # TenGigabitEthernet (SFP+)
    # --------------------------------------------------
    if sfp and port <= fe + ge + sfp:
        sfp_port = port - fe - ge
        return "TenGigabitEthernet", f"1/0/{sfp_port}"

    raise ValueError(
        f"Port {port} out of range for model {model} "
        f"(max {fe + ge + sfp})"
    )




def parse_interface(output: str) -> dict:
    # UP / DOWN (не только connected!)
    status_match = re.search(r"is\s+(up|down)", output, re.I)
    status = status_match.group(1).lower() if status_match else "down"

    if status != "up":
        return {"status": "down"}

    duplex_speed_match = re.search(
        r"(Full|Half)-duplex,\s+(\d+Mbps).*?media type is ([^\n]+)",
        output,
        re.I,
    )

    input_match = re.search(r"15 second input rate is (\d+) Kbit/s", output)
    output_match = re.search(r"15 second output rate is (\d+) Kbit/s", output)

    input_errors_match = re.search(r"(\d+) input errors", output)
    output_errors_match = re.search(r"(\d+) output errors", output)

    return {
        "status": "up",
        "duplex": duplex_speed_match.group(1) if duplex_speed_match else "Unknown",
        "link_speed": duplex_speed_match.group(2) if duplex_speed_match else "Unknown",
        "media_type": duplex_speed_match.group(3).strip() if duplex_speed_match else "Unknown",
        "input_rate": input_match.group(1) if input_match else "0",
        "output_rate": output_match.group(1) if output_match else "0",
        "input_errors": input_errors_match.group(1) if input_errors_match else "0",
        "output_errors": output_errors_match.group(1) if output_errors_match else "0",
    }
