SHOW_UNCFG = "show gpon onu uncfg"
SHOW_BY_SN = "show gpon onu by sn {serial}"
SHOW_ONU_CFG = "show running-config interface gpon-onu_{iface}"

# IP STATUS sources
SHOW_IP_SERVICE = "show ip-service user status gpon-onu_{iface}"
SHOW_DHCP_SNOOPING = (
    "show ip dhcp snooping dynamic port pon gpon-onu_{iface} sport 1"
)

SHOW_PON_POWER = "show pon power attenuation gpon-onu_{iface}"
