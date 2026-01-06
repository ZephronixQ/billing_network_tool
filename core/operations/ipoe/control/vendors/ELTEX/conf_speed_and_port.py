import asyncio

from core.connection.telnet import send_ipoe
from core.operations.ipoe.control.base import BaseIPoEController
from core.operations.ipoe.adapter.ELTEX.parsers.eltex_ipoe_interface import (
    resolve_eltex_interface,
)


class ELTEXPortController(BaseIPoEController):
    vendor = "ELTEX"

    VALID_SPEEDS = {
        "10",
        "100",
        "1000",
        "10000",
    }

    def __init__(self, reader, writer):
        super().__init__(reader, writer)
        self._enabled = False
        self.model: str | None = None

    # model может быть установлен, но НЕ обязателен
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

        # --------------------------------------------------
        # 🚫 Запрет service / uplink портов
        # --------------------------------------------------
        if port >= 49:
            raise ValueError(
                f"Port {port} is not an access port on ELTEX devices"
            )

        # --------------------------------------------------
        # 1️⃣ Порты 25–28 → GigabitEthernet 1–4 (28p)
        # --------------------------------------------------
        if 25 <= port <= 28:
            await send_ipoe(
                self.reader,
                self.writer,
                [
                    "configure terminal",
                    f"interface GigabitEthernet 1/0/{port - 24}",
                ]
            )
            return

        # --------------------------------------------------
        # 2️⃣ Порты 1–24 → пробуем FastEthernet
        # --------------------------------------------------
        if port <= 24:
            output = await send_ipoe(
                self.reader,
                self.writer,
                [
                    "configure terminal",
                    f"interface FastEthernet 1/0/{port}",
                ]
            )

            # если FE существует — используем его
            if "(config-if)" in output:
                return

        # --------------------------------------------------
        # 3️⃣ Fallback → GigabitEthernet (52p или FE нет)
        # --------------------------------------------------
        await send_ipoe(
            self.reader,
            self.writer,
            [
                "configure terminal",
                f"interface GigabitEthernet 1/0/{port}",
            ]
        )

    async def _exit_interface(self):
        await send_ipoe(
            self.reader,
            self.writer,
            ["exit", "exit"]
        )

    async def disable_port(self, port):
        await self._ensure_enable()
        await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, ["shutdown"])
        await self._exit_interface()

    async def enable_port(self, port):
        await self._ensure_enable()
        await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, ["no shutdown"])
        await self._exit_interface()

    async def restart_port(self, port):
        await self._ensure_enable()
        await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, ["shutdown"])
        await asyncio.sleep(1)
        await send_ipoe(self.reader, self.writer, ["no shutdown"])
        await self._exit_interface()

    async def set_port_speed(self, port, speed: str):
        if speed not in self.VALID_SPEEDS:
            raise ValueError(
                f"Unsupported ELTEX speed mode: {speed}"
            )

        await self._ensure_enable()
        await self._enter_interface(port)
        await send_ipoe(self.reader, self.writer, [f"speed {speed}"])
        await self._exit_interface()
