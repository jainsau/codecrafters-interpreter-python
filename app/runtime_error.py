from .scanner import ValidTokenType


class RuntimeError_(RuntimeError):
    def __init__(self, token: ValidTokenType, message: str):
        self.token = token
        super().__init__(message)
