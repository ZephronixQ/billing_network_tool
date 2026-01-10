import asyncio
from core.connection.telnet import send_ipoe
from core.operations.ipoe.control.base import BaseIPoEController

class DLINKPortController(BaseIPoEController):
    vendor = "DLINK"
    VALID_SPEEDS = {
        "10_half",
        "10_full",
        "100_half",
        "100_full",
        "1000_full",
        "auto",
    }

    def __init__(self, reader, writer):
        super().__init__(reader, writer)
        self._enabled = False
        self.model: str | None = None

    def set_model(self, model: str):
        self.model = model

    async def _ensure_enable(self):
        if self._enabled:
            return

        output = await send_ipoe(
            self.reader,
            self.writer,
            ["enable"]
        )

        if "password" in output.lower():
            await send_ipoe(
                self.reader,
                self.writer,
                [""]
            )

        self._enabled = True

    async def _enter_interface(self, port: int | str):
        port = int(port)
        return port

    async def disable_port(self, port):
        await self._ensure_enable()
        port = await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, [f"config ports {port} state disable"])

    async def enable_port(self, port):
        await self._ensure_enable()
        port = await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, [f"config ports {port} state enable"])

    async def restart_port(self, port):
        await self._ensure_enable()
        port = await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, [f"config ports {port} state disable"])
        await asyncio.sleep(1)
        await send_ipoe(self.reader, self.writer, [f"config ports {port} state enable"])

    async def set_port_speed(self, port, speed: str):
        if speed not in self.VALID_SPEEDS:
            raise ValueError(f"Unsupported D-Link speed mode: {speed}")

        await self._ensure_enable()
        port = await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, [f"config ports {port} speed {speed}"])
