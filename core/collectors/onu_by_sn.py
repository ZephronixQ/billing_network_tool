import asyncio
from typing import Optional, Dict

from core.settings import SEM
from core.telnet.connection import telnet_connect
from core.telnet.commands import send_command_fast
from core.utils import clean_line
from core.regex import GPON_SN_REGEX, REMOTE_ID_REGEX


def parse_onu_interface(output: str) -> Optional[str]:
    for raw in output.splitlines():
        line = clean_line(raw)
        m = GPON_SN_REGEX.search(line)
        if m:
            return m.group(1)
    return None


def parse_remote_id(output: str) -> Optional[str]:
    for raw in output.splitlines():
        line = clean_line(raw)
        m = REMOTE_ID_REGEX.search(line)
        if m:
            return m.group(1)
    return None


async def search_onu_on_switch(
    host: str,
    serial: str
) -> Optional[Dict[str, str]]:

    async with SEM:
        try:
            reader, writer = await telnet_connect(host)

            output = await send_command_fast(
                reader, writer,
                f"show gpon onu by sn {serial}"
            )

            iface = parse_onu_interface(output)
            if not iface:
                writer.close()
                return None

            cfg = await send_command_fast(
                reader, writer,
                f"show running-config interface gpon-onu_{iface}"
            )

            remote_id = parse_remote_id(cfg)

            writer.close()
            await writer.wait_closed()

            return {
                "host": host,
                "serial": serial,
                "interface": iface,
                "remote_id": remote_id
            }

        except Exception:
            return None


async def find_onu_by_serial(
    switches: list[str],
    serial: str
) -> Optional[Dict[str, str]]:

    tasks = [
        asyncio.create_task(search_onu_on_switch(sw, serial))
        for sw in switches
    ]

    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            for t in tasks:
                t.cancel()
            return result

    return None
