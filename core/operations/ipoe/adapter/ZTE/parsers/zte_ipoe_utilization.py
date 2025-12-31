import re

def parse_port_utilization(raw: str) -> dict:
    util = re.search(
        r'Port\s+utilization\s*:\s*'
        r'input\s*([\d.,]+)%\s*,\s*output:\s*([\d.,]+)%',
        raw,
        re.I
    )

    input_val = output_val = "0.00%"

    if util:
        input_val = f"{float(util.group(1).replace(',', '.')):.2f}%"
        output_val = f"{float(util.group(2).replace(',', '.')):.2f}%"

    return {
        "input": input_val,
        "output": output_val,
    }
