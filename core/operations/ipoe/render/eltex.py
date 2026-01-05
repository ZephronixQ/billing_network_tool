from core.operations.ipoe.adapter.ELTEX.tables.eltex_report import print_port_report
from core.operations.ipoe.render.renderer_base import BaseIPoERenderer


class ELTEXRenderer(BaseIPoERenderer):
    def render(self, data: dict, port: int):
        print_port_report(port, data)
