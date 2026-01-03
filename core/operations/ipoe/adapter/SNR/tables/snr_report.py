from .snr_device import print_device_info
from .snr_port import print_port_status
from .snr_traffic import print_port_traffic
from .snr_errors import print_port_errors
from .snr_mac import print_mac
from .snr_logs import print_logs

def print_port_report(port, model, iface, mac, logs):
    print_device_info(model)

    if not print_port_status(port, iface):
        print_logs(logs)
        return

    print_port_traffic(iface)
    print_port_errors(iface)
    print_mac(mac)
    print_logs(logs)
