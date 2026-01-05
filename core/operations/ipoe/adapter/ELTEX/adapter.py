from core.operations.ipoe.adapter.base import BaseIPoEAdapter
from core.connection.telnet import send_ipoe_eltex
from .query import build_query_plan

class ELTEXIPoEAdapter(BaseIPoEAdapter):
    async def collect(self, port: int) -> dict:
        plan = build_query_plan(str(port))

        result: dict = {}
        context: dict = {}

        for step in plan:
            key = step["key"]
            commands = step.get("commands")
            parser = step["parser"]

            # --------------------------------------------------
            # COMMAND RESOLUTION
            # --------------------------------------------------
            if callable(commands):
                commands = commands(context)

            # --------------------------------------------------
            # NO COMMANDS (e.g. logs)
            # --------------------------------------------------
            if not commands:
                value = parser(self.reader, self.writer, context)
                if hasattr(value, "__await__"):
                    value = await value
                result[key] = value
                context[key] = value
                continue

            # --------------------------------------------------
            # EXECUTE COMMANDS
            # --------------------------------------------------
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
