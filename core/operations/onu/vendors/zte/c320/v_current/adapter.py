from core.connection.telnet import connect, send
from .commands import SHOW_UNCFG, SHOW_BY_SN, SHOW_ONU_CFG
from .parsers.uncfg import parse_uncfg
from .parsers.search import parse_onu_interface, parse_remote_id


class ZTEC320Adapter:
    async def fetch_uncfg(self, host: str):
        reader, writer = await connect(host)
        await send(reader, writer, "terminal length 0")
        output = await send(reader, writer, SHOW_UNCFG)
        writer.close()
        await writer.wait_closed()
        return parse_uncfg(output)

    async def search_by_sn(self, host: str, serial: str):
        reader, writer = await connect(host)
        await send(reader, writer, "terminal length 0")

        output = await send(reader, writer, SHOW_BY_SN.format(serial=serial))
        iface = parse_onu_interface(output)

        if not iface:
            writer.close()
            return None

        cfg = await send(reader, writer, SHOW_ONU_CFG.format(iface=iface))
        remote_id = parse_remote_id(cfg)

        writer.close()
        return {
            "host": host,
            "port": iface,
            "serial": serial,
            "remote_id": remote_id,
        }
