# adapter.py

from core.connection.telnet import connect, send_bulk

from core.operations.onu.commands.zte_zxan import (
    SHOW_BY_SN,
    SHOW_ONU_CFG,
    SHOW_IP_SERVICE,
    SHOW_DHCP_SNOOPING,
)

from ..parsers.search import parse_onu_interface, parse_remote_id
from ..parsers.ip_status import parse_ip_status


class ZteZxanOltAdapter:
    async def search_by_sn(self, host: str, serial: str):
        reader, writer = await connect(host)
        await send_bulk(reader, writer, ["terminal length 0"])

        # 1️⃣ ищем ONU по SN
        raw = await send_bulk(
            reader,
            writer,
            [SHOW_BY_SN.format(serial=serial)],
        )

        iface = parse_onu_interface(raw)
        if not iface:
            writer.close()
            await writer.wait_closed()
            return None

        # 2️⃣ один bulk-запрос по найденному iface
        raw = await send_bulk(
            reader,
            writer,
            [
                SHOW_ONU_CFG.format(iface=iface),
                SHOW_DHCP_SNOOPING.format(iface=iface),
                SHOW_IP_SERVICE.format(iface=iface),
            ],
        )

        writer.close()
        await writer.wait_closed()

        return {
            "host": host,
            "port": iface,
            "serial": serial,
            "remote_id": parse_remote_id(raw),
            "ip_service": parse_ip_status(raw),
        }
