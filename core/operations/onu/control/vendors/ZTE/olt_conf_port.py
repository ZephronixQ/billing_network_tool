import asyncio
from core.connection.telnet import send_ipoe
from core.security.gpon_conf_auth import validate_token
from core.security.gpon_conf_logger import log_event
from config.secrets import SWITCHES

class ZTEInterfaceController:
    vendor = "ZTE"
    def __init__(self, reader, writer, host: str, interface: str, user_token: str):
        self.reader = reader
        self.writer = writer
        self.host = host
        self.interface = interface

        # --- Проверка пользователя ---
        valid, name_or_err = validate_token(user_token)
        if not valid:
            raise PermissionError(f"Unauthorized or invalid token: {name_or_err}")
        self.user = name_or_err

        # --- Проверка IP в списке SWITCHES ---
        if host not in SWITCHES:
            raise ValueError(f"Target OLT {host} is not in the allowed switches list")

        # CLI интерфейс
        self.cli_iface = f"gpon-olt_{interface}"

    async def disable_interface(self):
        commands = [
            "configure terminal",
            f"interface {self.cli_iface}",
            "shutdown",
            "exit",
            "end",
        ]
        await self._send_commands(commands, "disable")

    async def enable_interface(self):
        commands = [
            "configure terminal",
            f"interface {self.cli_iface}",
            "no shutdown",
            "exit",
            "end",
        ]
        await self._send_commands(commands, "enable")

    async def _send_commands(self, commands: list[str], action: str):
        try:
            await send_ipoe(self.reader, self.writer, commands)
            await asyncio.sleep(0.5)

            log_event(
                f"User: {self.user} | Host: {self.host} | Interface: {self.interface} | Action: {action}"
            )
        except Exception as e:
            log_event(
                f"User: {self.user} | Host: {self.host} | Interface: {self.interface} | Action: {action} | ERROR: {e}"
            )
            raise
