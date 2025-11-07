from object import object


class Environment:
    def __init__(self) -> None:
        self.store: dict[str, object.Object] = {}

    def get(self, name: str) -> object.Object | None:
        return self.store.get(name, None)

    def set(self, name: str, val: object.Object) -> object.Object:
        self.store[name] = val
        return val
