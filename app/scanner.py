import re
from enum import Enum, auto
from typing import Tuple, List


class ValidTokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    # Convenience
    EOF = auto()


class WhiteTokenType(Enum):
    NEWLINE = auto()
    WHITESPACE = auto()
    COMMENT = auto()


class ErrorTokenType(Enum):
    UNEXP_CHAR = auto()
    UNTERM_STR = auto()


class ValidToken:
    def __init__(self, type_: ValidTokenType, lexeme: str, literal: str, line: int):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return (
            f"{self.type.name} {self.lexeme} {self.literal if self.literal else 'null'}"
        )


class WhiteToken:
    def __init__(self, type_: WhiteTokenType, lexeme: str, line: int):
        self.type = type_
        self.lexeme = lexeme
        self.line = line


class ErrorToken:
    def __init__(self, type_: ErrorTokenType, lexeme: str, error: str, line):
        self.type = type_
        self.lexeme = lexeme
        self.error = error
        self.line = line

    def __str__(self):
        return f"[line {self.line}] Error: {self.error}"


class Scanner:
    def __init__(self, buffer: str):
        self.buffer = buffer
        self._tokens: List[ValidToken] = []
        self._whites: List[WhiteToken] = []
        self._errors: List[ErrorToken] = []

    @property
    def tokens(self) -> Tuple[List[ValidToken], List[ErrorToken]]:
        self._scan()
        return self._tokens, self._errors

    def _scan(self) -> None:
        i, line = 0, 1
        while i < len(self.buffer):
            buffer = self.buffer[i:]
            match buffer:
                case _ if (m := re.match(r"\(", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.LEFT_PAREN, t, None, line)
                case _ if (m := re.match(r"\)", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.RIGHT_PAREN, t, None, line)
                case _ if (m := re.match(r"{", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.LEFT_BRACE, t, None, line)
                case _ if (m := re.match(r"}", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.RIGHT_BRACE, t, None, line)
                case _ if (m := re.match(r",", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.COMMA, t, None, line)
                case _ if (m := re.match(r"\.", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.DOT, t, None, line)
                case _ if (m := re.match(r"-", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.MINUS, t, None, line)
                case _ if (m := re.match(r"\+", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.PLUS, t, None, line)
                case _ if (m := re.match(r";", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.SEMICOLON, t, None, line)
                case _ if (m := re.match(r"\*", buffer)):
                    t = m.group()
                    token = ValidToken(ValidTokenType.STAR, t, None, line)
                case _ if buffer.startswith("!"):
                    if len(buffer) >= 2 and buffer[1] == "=":
                        token = ValidToken(ValidTokenType.BANG_EQUAL, "!=", None, line)
                    else:
                        token = ValidToken(ValidTokenType.BANG, "!", None, line)
                case _ if buffer.startswith("="):
                    if len(buffer) >= 2 and buffer[1] == "=":
                        token = ValidToken(ValidTokenType.EQUAL_EQUAL, "==", None, line)
                    else:
                        token = ValidToken(ValidTokenType.EQUAL, "=", None, line)
                case _ if buffer.startswith(">"):
                    if len(buffer) >= 2 and buffer[1] == "=":
                        token = ValidToken(
                            ValidTokenType.GREATER_EQUAL, ">=", None, line
                        )
                    else:
                        token = ValidToken(ValidTokenType.GREATER, ">", None, line)
                case _ if buffer.startswith("<"):
                    if len(buffer) >= 2 and buffer[1] == "=":
                        token = ValidToken(ValidTokenType.LESS_EQUAL, "<=", None, line)
                    else:
                        token = ValidToken(ValidTokenType.LESS, "<", None, line)
                case _ if (m := re.match(r"\"([^\"]*)\"", buffer)):
                    # match strings
                    t = m.group()
                    token = ValidToken(ValidTokenType.STRING, t, m.group(1), line)
                case _ if (m := re.match(r"([\d]+)\.?([\d]*)", buffer)):
                    # match number literals
                    # handle trailing zeros sensibly
                    t = m.group()
                    if (fraction := re.sub(r"0+$", r"", f"{m.group(2)}")) == "":
                        fraction = "0"
                    token = ValidToken(
                        ValidTokenType.NUMBER, t, f"{m.group(1)}.{fraction}", line
                    )
                case _ if (m := re.match(r"[A-z_][\w]*", buffer)):
                    # match keywords and identifiers
                    t = m.group()
                    if t in [
                        "and",
                        "class",
                        "else",
                        "false",
                        "fun",
                        "for",
                        "if",
                        "nil",
                        "or",
                        "print",
                        "return",
                        "super",
                        "this",
                        "true",
                        "var",
                        "while",
                    ]:
                        token = ValidToken(
                            getattr(ValidTokenType, t.upper()), t, None, line
                        )
                    else:
                        token = ValidToken(ValidTokenType.IDENTIFIER, t, None, line)
                case _ if (m := re.match(r"[\n]+", buffer)):
                    # match newline character(s)
                    t = m.group()
                    token = WhiteToken(WhiteTokenType.NEWLINE, t, line)
                    line += len(t)
                case _ if (m := re.match(r"[ \t]+", buffer)):
                    # match contiguous tabs and spaces
                    t = m.group()
                    token = WhiteToken(WhiteTokenType.WHITESPACE, t, line)
                case _ if buffer.startswith("/"):
                    if m := re.match(r"//.+", buffer):
                        # match comment
                        t = m.group()
                        token = WhiteToken(WhiteTokenType.COMMENT, t, line)
                    else:
                        token = ValidToken(ValidTokenType.SLASH, "/", None, line)
                case _ if (m := re.match(r"\"[^\"\n]*", buffer)):
                    # match unbalanced strings (error)
                    t = m.group()
                    token = ErrorToken(
                        ErrorTokenType.UNTERM_STR, t, "Unterminated string.", line
                    )
                case _:
                    t = buffer[0]
                    token = ErrorToken(
                        ErrorTokenType.UNEXP_CHAR, t, f"Unexpected character: {t}", line
                    )

            if token.type in ValidTokenType:
                self._tokens.append(token)
            elif token.type in ErrorTokenType:
                self._errors.append(token)
            else:
                self._whites.append(token)

            i += len(token.lexeme)

        self._tokens.append(ValidToken(ValidTokenType.EOF, "", None, line))
