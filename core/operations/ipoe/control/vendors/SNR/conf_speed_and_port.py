import asyncio
from core.connection.telnet import send_ipoe
from core.operations.ipoe.control.base import BaseIPoEController

class SNRPortController(BaseIPoEController):
    vendor = "SNR"
    VALID_SPEEDS = {
        "auto",
        "force10-full",
        "force10-half",
        "force100-full",
        "force100-fx",
        "force100-half",
        "force1g-full",
        "force1g-half",
        "force10g-full",
    }

    def __init__(self, reader, writer):
        super().__init__(reader, writer)
        self._enabled = False

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

    async def _enter_interface(self, port: str):
        await send_ipoe(
            self.reader,
            self.writer,
            [
                "config terminal",
                f"interface ethernet 1/0/{port}",
            ]
        )

    async def _exit_interface(self):
        await send_ipoe(
            self.reader,
            self.writer,
            [
                "exit",
                "exit",
            ]
        )

    async def disable_port(self, port: str):
        await self._ensure_enable()
        await self._enter_interface(port)

        await send_ipoe(
            self.reader,
            self.writer,
            ["shutdown"]
        )

        await self._exit_interface()

    async def enable_port(self, port: str):
        await self._ensure_enable()
        await self._enter_interface(port)

        await send_ipoe(
            self.reader,
            self.writer,
            ["no shutdown"]
        )

        await self._exit_interface()

    async def restart_port(self, port: str):
        await self._ensure_enable()
        await self._enter_interface(port)

        await send_ipoe(
            self.reader,
            self.writer,
            ["shutdown"]
        )

        await asyncio.sleep(1)

        await send_ipoe(
            self.reader,
            self.writer,
            ["no shutdown"]
        )

        await self._exit_interface()

    async def set_port_speed(self, port: str, speed: str):
        if speed not in self.VALID_SPEEDS:
            raise ValueError(
                f"Unsupported SNR speed mode: {speed}"
            )

        await self._ensure_enable()
        await self._enter_interface(port)

        await send_ipoe(
            self.reader,
            self.writer,
            [f"speed-duplex {speed}"]
        )

        await self._exit_interface()
