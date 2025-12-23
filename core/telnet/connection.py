import asyncio
import telnetlib3
import logging
from typing import Tuple
from config.credentials import USERNAME, PASSWORD, TELNET_PORT


async def telnet_connect(
    host: str,
    retries: int = 3
) -> Tuple[telnetlib3.TelnetReader, telnetlib3.TelnetWriter]:

    for attempt in range(1, retries + 1):
        try:
            reader, writer = await telnetlib3.open_connection(
                host=host,
                port=TELNET_PORT,
                connect_minwait=0.05,
                connect_maxwait=0.2
            )
            writer.write(USERNAME + "\n")
            writer.write(PASSWORD + "\n")
            return reader, writer

        except Exception as e:
            logging.warning(f"[{host}] Attempt {attempt}/{retries} failed: {e}")
            await asyncio.sleep(0.1 * attempt)

    raise ConnectionError(f"[{host}] Connection failed")