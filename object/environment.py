from object import object


class Environment:
    def __init__(self, outer: 'Environment | None' = None) -> None:
        self.store: dict[str, object.Object] = {}
        self.outer = outer

    def get(self, name: str) -> object.Object | None:
        obj = self.store.get(name)
        if obj is None and self.outer is not None:
            return self.outer.get(name)
        return obj

    def set(self, name: str, val: object.Object) -> object.Object:
        self.store[name] = val
        return val
