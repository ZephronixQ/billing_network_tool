import asyncio

from core.connection.telnet import connect, send_bulk

from core.operations.onu.commands.zte_zxan import (
    SHOW_BY_SN,
    SHOW_ONU_CFG,
    SHOW_IP_SERVICE,
    SHOW_DHCP_SNOOPING,
    SHOW_PON_POWER,
    SHOW_STATUS,
    SHOW_INTERFACE,
)

from core.operations.onu.parsers.search import (
    parse_onu_interface,
    parse_remote_id,
)
from core.operations.onu.parsers.ip_status import parse_ip_status
from core.operations.onu.parsers.pon_power import parse_pon_power
from core.operations.onu.parsers.speed import (
    parse_remote_onu_interface,
    parse_interface_speed,
)


class ZteZxanOltAdapter:
    async def search_by_sn(self, host: str, serial: str):
        reader, writer = await connect(host)

        try:
            # =========================================================
            # FLUSH CLI (WELCOME / PROMPT / NOISE)
            # =========================================================
            try:
                while True:
                    await asyncio.wait_for(reader.read(4096), 0.3)
            except asyncio.TimeoutError:
                pass

            # =========================================================
            # 1. SEARCH ONU (MINIMAL & CLEAN)
            # =========================================================
            raw_find = await send_bulk(
                reader,
                writer,
                [
                    "terminal length 0",
                    SHOW_BY_SN.format(serial=serial),
                ],
                timeout=3.0,
            )

            iface = parse_onu_interface(raw_find)
            if not iface:
                return None

            # =========================================================
            # 2. COLLECT ALL DATA (ONE SESSION)
            # =========================================================
            raw_all = await send_bulk(
                reader,
                writer,
                [
                    SHOW_ONU_CFG.format(iface=iface),
                    SHOW_IP_SERVICE.format(iface=iface),
                    SHOW_DHCP_SNOOPING.format(iface=iface),
                    SHOW_PON_POWER.format(iface=iface),
                    SHOW_STATUS.format(iface=iface),
                    SHOW_INTERFACE.format(iface=iface),
                ],
                timeout=5.0,
            )

            # =========================================================
            # 3. PARSING
            # =========================================================
            remote_id = parse_remote_id(raw_all)

            ip_service = (
                parse_ip_status(raw_all)
                or {"ip": "-", "mac": "-", "vlan": "-"}
            )

            pon_power = parse_pon_power(raw_all)

            remote_onu = parse_remote_onu_interface(raw_all)
            iface_speed = parse_interface_speed(raw_all)

            # =========================================================
            # 4. RESULT
            # =========================================================
            return {
                "host": host,
                "port": iface,
                "serial": serial,
                "remote_id": remote_id,
                "ip_service": ip_service,
                "pon_power": pon_power,
                "remote_onu": remote_onu,
                "iface_speed": iface_speed,
            }

        finally:
            writer.close()
            await writer.wait_closed()
