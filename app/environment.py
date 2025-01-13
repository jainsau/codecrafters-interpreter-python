from .scanner import ValidToken
from .error import RuntimeError_


class Environment:
    def __init__(self):
        self.values = dict()

    def get(self, name: ValidToken) -> object:
        try:
            return self.values[name.lexeme]
        except KeyError:
            raise RuntimeError_(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: object) -> None:
        self.values[name] = value
