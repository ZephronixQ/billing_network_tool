import logging, asyncio
from typing import Optional, Dict, List

from core.settings import SEM
from core.telnet.connection import telnet_connect
from core.telnet.commands import send_command_fast
from core.utils import parse_uncfg_onu


async def get_uncfg_onu_from_switch(
    host: str
) -> Optional[Dict[str, List[Dict[str, str]]]]:

    async with SEM:
        try:
            reader, writer = await telnet_connect(host)

            await send_command_fast(reader, writer, "terminal length 0")
            output = await send_command_fast(reader, writer, "show gpon onu uncfg")

            writer.close()
            await writer.wait_closed()

            onus = parse_uncfg_onu(output)
            return {"host": host, "onus": onus} if onus else None

        except Exception as e:
            logging.error(f"[{host}] Error: {e}")
            return None


async def collect_all_uncfg_onu(
    switches: List[str]
) -> List[Dict[str, List[Dict[str, str]]]]:

    tasks = [get_uncfg_onu_from_switch(sw) for sw in switches]
    results = await asyncio.gather(*tasks)

    return [r for r in results if r]