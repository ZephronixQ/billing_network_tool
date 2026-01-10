from core.operations.ipoe.adapter.DLink.tables.dlink_report import print_port_report
from core.operations.ipoe.render.renderer_base import BaseIPoERenderer

class DlinkRenderer(BaseIPoERenderer):

    def render(self, data: dict, port: int):
        print_port_report(port, data)
