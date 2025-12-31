from abc import ABC, abstractmethod


class BaseIPoEAdapter(ABC):
    """
    Базовый контракт для IPOE адаптеров
    """

    vendor: str

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    @abstractmethod
    async def collect(self, port: str) -> dict:
        """
        Возвращает нормализованные данные IPOE
        """
        ...
