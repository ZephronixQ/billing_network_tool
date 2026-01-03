SNR_MODEL_PORTS = {
    "S2965-8T": (8, 2),
    "S2965-24T": (24, 4),
    "S2985G-48T": (48, 4),
}

SNR_LOG_INCLUDE_MODELS = {
    "S2965-8T",
    "S2965-24T",
}

PROMPT = "#"

def format_ports(fe: int, ge: int) -> str:
    if fe and ge:
        return f"{fe}FE + {ge}GE ({fe + ge})"
    if ge:
        return f"{ge}GE ({ge})"
    if fe:
        return f"{fe}FE ({fe})"
    return "N/A"