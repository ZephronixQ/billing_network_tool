# renderer_base.py
from abc import ABC, abstractmethod

class BaseIPoERenderer(ABC):

    @abstractmethod
    def render(self, data: dict, port: str) -> None:
        ...
