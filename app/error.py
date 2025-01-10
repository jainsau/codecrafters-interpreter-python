from app.scanner import ValidTokenType


class ParseError(RuntimeError):
    pass


class RuntimeError_(RuntimeError):
    def __init__(self, token: ValidTokenType, message: str):
        self.token = token
        super().__init__(message)
