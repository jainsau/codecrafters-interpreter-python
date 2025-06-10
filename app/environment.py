from .error import RuntimeError_
from .scanner import ValidToken
from typing import Optional


class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.enclosing = enclosing
        self.values = dict()

    def get(self, name: ValidToken) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing:
            return self.enclosing.get(name)
        else:
            raise RuntimeError_(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def assign(self, name: ValidToken, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        elif self.enclosing:
            self.enclosing.assign(name, value)
            return
        else:
            raise RuntimeError_(name, f"Undefined variable '{name.lexeme}'.")
