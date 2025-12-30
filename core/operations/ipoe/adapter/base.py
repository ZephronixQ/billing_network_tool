from abc import ABC, abstractmethod


class BaseIPoEAdapter(ABC):

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    @abstractmethod
    async def run(self) -> dict:
        """
        Возвращает:
        {
            vendor: str,
            model: str,
            ports: int,
            speed: str,
            port: {
                state: str,
                speed: str,
                uptime: str
            }
        }
        """
        ...
