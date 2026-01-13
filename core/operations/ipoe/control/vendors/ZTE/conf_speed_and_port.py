import asyncio

from core.connection.telnet import send_ipoe
from core.operations.ipoe.control.base import BaseIPoEController

class ZTEPortController(BaseIPoEController):
    vendor = "ZTE"

    def __init__(self, reader, writer):
        super().__init__(reader, writer)
        self._enabled = False

    async def _ensure_enable(self):
        if self._enabled:
            return

        output = await send_ipoe(
            self.reader,
            self.writer,
            ["en"],
            timeout=1.0
        )

        if "password" in output.lower():
            output = await send_ipoe(
                self.reader,
                self.writer,
                [""],
                timeout=1.0
            )

        if "(cfg)#" not in output and "#" not in output:
            raise RuntimeError(
                "Failed to enter enable mode on ZTE device"
            )

        self._enabled = True

    async def collect(self, port: str) -> dict:
        return {}

    async def disable_port(self, port: str):
        await self._ensure_enable()
        await send_ipoe(
            self.reader,
            self.writer,
            [f"set port {port} disable"]
        )

    async def enable_port(self, port: str):
        await self._ensure_enable()
        await send_ipoe(
            self.reader,
            self.writer,
            [f"set port {port} enable"]
        )

    async def restart_port(self, port: str):
        await self._ensure_enable()
        await self.disable_port(port)
        await asyncio.sleep(1)
        await self.enable_port(port)

    async def set_port_speed(self, port: str, speed: int):
        if speed not in (10, 100):
            raise ValueError("Supported speeds: 10, 100")

        await self._ensure_enable()
        await send_ipoe(
            self.reader,
            self.writer,
            [f"set port {port} speed {speed}"]
        )
