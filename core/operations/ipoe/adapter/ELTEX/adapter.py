from core.operations.ipoe.adapter.base import BaseIPoEAdapter
from core.connection.telnet import send_ipoe_eltex
from .query import build_query_plan

class ELTEXIPoEAdapter(BaseIPoEAdapter):
    async def collect(self, port: int) -> dict:
        plan = build_query_plan(port)  # <-- БЕЗ str()

        result: dict = {}
        context: dict = {}

        for step in plan:
            key = step["key"]
            commands = step.get("commands")
            parser = step["parser"]

            if callable(commands):
                commands = commands(context)

            if commands is None:
                result[key] = []
                context[key] = []
                continue

            raw = await send_ipoe_eltex(
                self.reader,
                self.writer,
                commands,
            )

            try:
                value = parser(raw, context)
            except TypeError:
                value = parser(raw)

            result[key] = value
            context[key] = value

        return result
