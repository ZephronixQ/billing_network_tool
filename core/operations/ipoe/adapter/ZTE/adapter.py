from core.connection.telnet import connect
from .commands import BASE_COMMANDS, PORT_COMMAND
from .parsers import parse_device_info, parse_port_info
from ..session import send_command


class ZTEIPoeAdapter:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    async def run(self) -> dict:
        reader, writer = await connect(self.host)

        # paging off
        for cmd in BASE_COMMANDS:
            await send_command(reader, writer, cmd)

        version_out = await send_command(reader, writer, "show version")
        port_out = await send_command(reader, writer, PORT_COMMAND(self.port))

        writer.close()

        device = parse_device_info(version_out)
        port = parse_port_info(port_out)

        return {
            "device": device,
            "port": port,
        }
