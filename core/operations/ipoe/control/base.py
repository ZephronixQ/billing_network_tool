from abc import ABC, abstractmethod


class BaseIPoEController(ABC):
    vendor: str

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    @abstractmethod
    async def disable_port(self, port: str):
        ...

    @abstractmethod
    async def enable_port(self, port: str):
        ...

    @abstractmethod
    async def restart_port(self, port: str):
        ...

    @abstractmethod
    async def set_port_speed(self, port: str, speed: int):
        ...
