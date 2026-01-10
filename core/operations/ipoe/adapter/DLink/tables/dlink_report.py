from .dlink_device import print_device_info, format_ports
from .dlink_port import print_port_status
from .dlink_stats import print_port_stats
from .dlink_mac import print_mac
from .dlink_logs import print_logs

def print_port_report(port: int, info: dict):
    print_device_info(info)
    print_port_status(port, info)
    print_port_stats(info)
    print_mac(info)
    print_logs(info)
    print()
