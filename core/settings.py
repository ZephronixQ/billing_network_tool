import asyncio
from config.devices import SWITCHES

SEM: asyncio.Semaphore = asyncio.Semaphore(len(SWITCHES))