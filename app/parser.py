from app import lox
from app.error import ParseError
from app.expr import Expr, Binary, Unary, Literal, Grouping
from app.scanner import ValidToken, ValidTokenType
from app.stmt import Stmt, Print, Expression
from typing import List, Optional


class Parser:
    def __init__(self, tokens: List[ValidToken]):
        self.tokens = tokens
        self.cursor = 0
        self.statements = []

    def error(self, token: ValidToken, message: str) -> ParseError:
        lox.Lox.error2(token, message)

        return ParseError()

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().type == ValidTokenType.SEMICOLON:
                return
            match self.peek().type:
                case ValidTokenType.PRINT:
                    return

            self.advance()

    def peek(self) -> ValidToken:
        return self.tokens[self.cursor]

    def is_at_end(self) -> bool:
        return self.peek().type == ValidTokenType.EOF

    def previous(self) -> ValidToken:
        return self.tokens[self.cursor - 1]

    def advance(self) -> ValidToken:
        if not self.is_at_end():
            self.cursor += 1
        self.previous()

    def check(self, type_: ValidTokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def match(self, *types: ValidTokenType) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def consume(self, type_: ValidTokenType, message: str) -> ValidToken:
        if self.check(type_):
            return self.advance()

        raise self.error(self.peek(), message)

    def expr(self) -> Optional[Expr]:
        try:
            return self.equality()
        except ParseError:
            return None

    def parse(self) -> Optional[Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    def declaration(self) -> Stmt:
        try:
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self) -> Stmt:
        if self.match(ValidTokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(ValidTokenType.SEMICOLON, "Expect ';' after value.")

        return Print(value)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(ValidTokenType.SEMICOLON, "Expect ';' after expression.")

        return Expression(expr)

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(
            ValidTokenType.BANG_EQUAL,
            ValidTokenType.EQUAL_EQUAL,
        ):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(
            ValidTokenType.GREATER,
            ValidTokenType.GREATER_EQUAL,
            ValidTokenType.LESS,
            ValidTokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(
            ValidTokenType.MINUS,
            ValidTokenType.PLUS,
        ):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(
            ValidTokenType.SLASH,
            ValidTokenType.STAR,
        ):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(
            ValidTokenType.BANG,
            ValidTokenType.MINUS,
        ):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(
            ValidTokenType.FALSE,
            ValidTokenType.TRUE,
            ValidTokenType.NIL,
            ValidTokenType.FLOAT,
            ValidTokenType.INTEGER,
            ValidTokenType.STRING,
        ):
            return Literal(self.previous())
        if self.match(ValidTokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(ValidTokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")
