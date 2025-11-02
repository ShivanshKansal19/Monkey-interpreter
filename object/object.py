from typing import NewType
from abc import ABC, abstractmethod

ObjectType = NewType('ObjectType', str)

INTEGER_OBJ = ObjectType('INTEGER')
BOOLEAN_OBJ = ObjectType('BOOLEAN')
NULL_OBJ = ObjectType('NULL')


class Object(ABC):
    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass


class Integer(Object):
    def __init__(self, value: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return INTEGER_OBJ

    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):
    def __init__(self, value: bool) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return BOOLEAN_OBJ

    def inspect(self) -> str:
        return 'true' if self.value else 'false'


class Null(Object):
    def __init__(self) -> None:
        self.value = 'null'

    def type(self) -> ObjectType:
        return NULL_OBJ

    def inspect(self) -> str:
        return self.value
