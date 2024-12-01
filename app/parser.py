from .scanner import ValidToken, ValidTokenType
from .expr import Expr, Literal, Grouping
from typing import List


class Parser:
    def __init__(self, tokens: List[ValidToken]):
        self.tokens = tokens
        self.cursor = 0

    @property
    def current_token(self):
        return self.tokens[self.cursor]

    def expression(self) -> Expr:
        return self.primary()

    def primary(self) -> Expr:
        match self.current_token.type:
            case ValidTokenType.FALSE:
                expr = Literal("false")
            case ValidTokenType.TRUE:
                expr = Literal("true")
            case ValidTokenType.NIL:
                expr = Literal(None)
            case ValidTokenType.NUMBER | ValidTokenType.STRING:
                expr = Literal(self.current_token.literal)
            case ValidTokenType.LEFT_PAREN:
                self.cursor += 1
                expr = self.expression()
                if self.current_token.type is ValidTokenType.RIGHT_PAREN:
                    expr = Grouping(expr)
                else:
                    raise Exception("Expect ')' after for clauses.")

        self.cursor += 1
        return expr
