from core.connection.telnet import send_ipoe_dlink
from core.operations.ipoe.adapter.base import BaseIPoEAdapter
from .query import build_query_plan
from .constants import DEVICE_MODEL_DB

class DLinkIPoeAdapter(BaseIPoEAdapter):
    async def collect(self, port: int) -> dict:
        plan = build_query_plan(port)
        result: dict = {}
        context: dict = {"reader": self.reader, "writer": self.writer}

        for step in plan:
            key = step["key"]
            commands = step.get("commands")
            parser = step["parser"]
            is_async = step.get("async", False)

            if callable(commands):
                commands = commands(context)

            if commands is None:
                result[key] = [] if key != "device" else "UNKNOWN"
                context[key] = result[key]
                continue

            if is_async:
                # Асинхронный парсер вызываем через await
                value = await parser(commands, context)
            else:
                raw = await send_ipoe_dlink(self.reader, self.writer, commands)
                try:
                    value = parser(raw, context)
                except TypeError:
                    value = parser(raw)

            result[key] = value
            context[key] = value


        model = result.get("device", "UNKNOWN")
        profile = DEVICE_MODEL_DB.get(model, {})

        return {
            "vendor": profile.get("vendor", "UNKNOWN"),
            "model": model,
            "ports": profile,
            "port": port,
            "port_state": result.get("port_info", ["DOWN", None])[0],
            "port_speed": result.get("port_info", ["DOWN", None])[1],
            "macs": result.get("macs", []),
            "traffic": {
                "rx_bytes": result.get("traffic", [0, 0])[0],
                "tx_bytes": result.get("traffic", [0, 0])[1],
            },
            "errors": dict(zip(
                ["rx_crc", "tx_crc", "rx_desc", "tx_desc"],
                result.get("errors", [0,0,0,0])
            )),
            "logs": result.get("logs", []),
        }
