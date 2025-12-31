SHOW_VERSION = ["show version"]

def show_port(port: str):
    return [f"show port {port}"]

def show_port_util(port: str):
    return [f"show port {port} utilization"]

def show_mac(port: str):
    return [f"show mac dynamic port {port}"]

SHOW_DHCP = ["show dhcp relay binding"]

def show_statistics(port: str):
    return [f"show port {port} statistics"]

def show_mac_protect(port: str):
    return [f"show mac protect port {port}"]

SHOW_LOGS = ["show terminal log include Port"]
