# ============================================================
# ELTEX IPOE COMMANDS
# ============================================================

# --- device ---
SHOW_SYSTEM_MES = "show system | include MES"
SHOW_VERSION = "show version"

# --- interface ---
SHOW_INTERFACE = "show interfaces {int_type} {port}"

# --- mac ---
SHOW_MAC_TABLE = "show mac address-table interface {int_type} {port}"

# --- logging ---
SHOW_LOGGING_INCLUDE = "show logging | include {short_port}"
