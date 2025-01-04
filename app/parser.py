from .scanner import ValidToken, ValidTokenType
from .expr import Expr, Binary, Unary, Literal, Grouping
from typing import Tuple, List, Optional


class ParseError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens: List[ValidToken]):
        self.tokens = tokens
        self.cursor = 0

    @property
    def current_token(self) -> Optional[ValidToken]:
        try:
            return self.tokens[self.cursor]
        except IndexError:
            return None

    def error(self, message: str) -> ParseError:
        raise ParseError

    def parse(self) -> Tuple[bool, Optional[Expr]]:
        try:
            return False, (
                None
                if self.current_token.type is ValidTokenType.EOF
                else self.expression()
            )
        except ParseError:
            return True, None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.current_token and self.current_token.type in [
            ValidTokenType.BANG_EQUAL,
            ValidTokenType.EQUAL_EQUAL,
        ]:
            operator = self.current_token
            self.cursor += 1
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.current_token and self.current_token.type in [
            ValidTokenType.GREATER,
            ValidTokenType.GREATER_EQUAL,
            ValidTokenType.LESS,
            ValidTokenType.LESS_EQUAL,
        ]:
            operator = self.current_token
            self.cursor += 1
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.current_token and self.current_token.type in [
            ValidTokenType.MINUS,
            ValidTokenType.PLUS,
        ]:
            operator = self.current_token
            self.cursor += 1
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.current_token and self.current_token.type in [
            ValidTokenType.SLASH,
            ValidTokenType.STAR,
        ]:
            operator = self.current_token
            self.cursor += 1
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.current_token and self.current_token.type in [
            ValidTokenType.BANG,
            ValidTokenType.MINUS,
        ]:
            operator = self.current_token
            self.cursor += 1
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        token = self.current_token
        match token.type:
            case (
                ValidTokenType.FALSE
                | ValidTokenType.TRUE
                | ValidTokenType.NIL
                | ValidTokenType.FLOAT
                | ValidTokenType.INTEGER
                | ValidTokenType.STRING
            ):
                expr = Literal(token)
            case ValidTokenType.LEFT_PAREN:
                self.cursor += 1
                expr = self.expression()
                if self.current_token.type is ValidTokenType.RIGHT_PAREN:
                    expr = Grouping(expr)
                else:
                    self.error("Expect ')' after for clauses.")
            case _:
                self.error("Expect expression.")

        self.cursor += 1
        return expr
