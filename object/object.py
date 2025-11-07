from typing import NewType
from abc import ABC, abstractmethod

ObjectType = NewType('ObjectType', str)

INTEGER_OBJ = ObjectType('INTEGER')
BOOLEAN_OBJ = ObjectType('BOOLEAN')
NULL_OBJ = ObjectType('NULL')
RETURN_VALUE_OBJ = ObjectType('RETURN_VALUE')
ERROR_OBJ = ObjectType('ERROR')


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
        pass

    def type(self) -> ObjectType:
        return NULL_OBJ

    def inspect(self) -> str:
        return 'null'


class ReturnValue(Object):
    def __init__(self, value: Object) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return RETURN_VALUE_OBJ

    def inspect(self) -> str:
        return self.value.inspect()


class Error(Object):
    def __init__(self, message: str) -> None:
        self.message = message

    def type(self) -> ObjectType:
        return ERROR_OBJ

    def inspect(self) -> str:
        return "ERROR: "+self.message
