# core/operations/onu/adapters/zte_zxan_olt.py

from core.connection.telnet import connect, send_bulk
from core.operations.onu.commands.zte_zxan import (
    SHOW_BY_SN,
    SHOW_ONU_CFG,
    SHOW_IP_SERVICE,
    SHOW_DHCP_SNOOPING,
    SHOW_PON_POWER,
)

from core.operations.onu.parsers.search import (
    parse_onu_interface,
    parse_remote_id,
)
from core.operations.onu.parsers.ip_status import parse_ip_status
from core.operations.onu.parsers.pon_power import parse_pon_power


class ZteZxanOltAdapter:
    async def search_by_sn(self, host: str, serial: str):
        reader, writer = await connect(host)

        try:
            # ========= SEARCH ONU =========
            raw_find = await send_bulk(
                reader,
                writer,
                [
                    "terminal length 0",
                    SHOW_BY_SN.format(serial=serial),
                ],
                timeout=2.0,
            )

            iface = parse_onu_interface(raw_find)
            if not iface:
                return None

            # ========= COLLECT ALL DATA (ONE SESSION) =========
            raw_all = await send_bulk(
                reader,
                writer,
                [
                    SHOW_ONU_CFG.format(iface=iface),
                    SHOW_IP_SERVICE.format(iface=iface),
                    SHOW_DHCP_SNOOPING.format(iface=iface),
                    SHOW_PON_POWER.format(iface=iface),
                ],
                timeout=3.0,
            )

            remote_id = parse_remote_id(raw_all)

            ip_service = (
                parse_ip_status(raw_all)
                or {"ip": "-", "mac": "-", "vlan": "-"}
            )

            pon_power = parse_pon_power(raw_all)

            return {
                "host": host,
                "port": iface,
                "serial": serial,
                "remote_id": remote_id,
                "ip_service": ip_service,
                "pon_power": pon_power,
            }

        finally:
            writer.close()
            await writer.wait_closed()
