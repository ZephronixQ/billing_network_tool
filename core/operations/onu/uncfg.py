import asyncio
from core.connection.telnet import connect, send
from core.parsers.onu import parse_uncfg
from output.table import print_uncfg_table
from config.secrets import SWITCHES

SEM = asyncio.Semaphore(len(SWITCHES))

async def fetch_uncfg(host):
    async with SEM:
        try:
            reader, writer = await connect(host)
            await send(reader, writer, "terminal length 0")
            output = await send(reader, writer, "show gpon onu uncfg")
            writer.close()
            await writer.wait_closed()
            onus = parse_uncfg(output)
            return {"host": host, "onus": onus} if onus else None
        except Exception:
            return None

async def run_uncfg():
    tasks = [fetch_uncfg(sw) for sw in SWITCHES]
    results = [r for r in await asyncio.gather(*tasks) if r]
    print_uncfg_table(results)