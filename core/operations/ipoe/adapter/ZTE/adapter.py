from core.operations.ipoe.adapter.base import BaseIPoEAdapter
from core.operations.ipoe.common.executor import execute_cli_plan
from .query import build_query_plan
from core.connection.telnet import send_ipoe

class ZTEIPoeAdapter(BaseIPoEAdapter):
    vendor = "ZTE"

    async def collect(self, port: str) -> dict:
        version = await send_ipoe(self.reader, self.writer, ["show version"])
        plan = build_query_plan(port)
        return await execute_cli_plan(self.reader, self.writer, plan)
