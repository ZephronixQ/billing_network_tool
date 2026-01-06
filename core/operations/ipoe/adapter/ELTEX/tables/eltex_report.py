from .eltex_device import print_device_info
from .eltex_port import print_port_status
from .eltex_stats import print_port_stats
from .eltex_mac import print_mac
from .eltex_logs import print_logs

def print_port_report(port: int, data: dict):
    device = data["device"]
    iface = data["interface"]
    mac = data.get("mac", [])
    logs = data.get("logs", [])

    print_device_info(device)

    if not print_port_status(port, iface):
        print_logs(logs)
        return

    print_port_stats(iface)
    print_mac(mac)
    print_logs(logs)

