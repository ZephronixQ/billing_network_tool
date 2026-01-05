import re


def determine_interface_type(speed: str) -> str:
    if speed.startswith("1G"):
        return "GigabitEthernet"
    return "FastEthernet"


def parse_interface(output: str) -> dict:
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
