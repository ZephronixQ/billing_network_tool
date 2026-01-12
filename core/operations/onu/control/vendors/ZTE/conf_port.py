import asyncio
from core.connection.telnet import send_ipoe

class ZTEPortController:
    vendor = "ZTE"

    def __init__(self, reader, writer, host: str, iface: str):
        self.reader = reader
        self.writer = writer
        self.host = host

        # --- нормализуем iface ---
        if iface.startswith("gpon-onu_"):
            iface = iface.replace("gpon-onu_", "")

        # теперь iface = "1/3/8:126"
        self.raw_iface = iface

        # split → olt_port + onu_id
        self.olt_port, self.onu_id = iface.split(":")

        # готовые CLI интерфейсы
        self.iface_onu = f"gpon-onu_{self.raw_iface}"
        self.iface_olt = f"gpon-olt_{self.olt_port}"

    async def disable_port(self):
        commands = [
            "configure terminal",
            f"interface {self.iface_onu}",
            "shutdown",
            "exit",
            "end",
        ]
        await send_ipoe(self.reader, self.writer, commands)

    async def enable_port(self):
        commands = [
            "configure terminal",
            f"interface {self.iface_onu}",
            "no shutdown",
            "exit",
            "end",
        ]
        await send_ipoe(self.reader, self.writer, commands)

    async def restart_port(self):
        await self.disable_port()
        await asyncio.sleep(1)
        await self.enable_port()

    async def delete_onu(self):
        commands = [
            "configure terminal",
            f"interface {self.iface_olt}",
            f"no onu {self.onu_id}",
            "exit",
            "end",
        ]
        await send_ipoe(self.reader, self.writer, commands)
