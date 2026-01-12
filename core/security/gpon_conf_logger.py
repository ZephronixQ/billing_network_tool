from pathlib import Path
import logging

LOG_FILE = Path(r"core\security\gpon_conf_actions.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8"
)

def log_event(message: str):
    logging.info(message)
