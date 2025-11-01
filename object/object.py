from typing import NewType
from abc import ABC, abstractmethod

ObjectType = NewType('ObjectType', str)


class Object(ABC):
    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass
