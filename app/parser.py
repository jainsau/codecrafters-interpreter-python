from app import lox
from app.error import ParseError
from app.expr import Expr, Assign, Binary, Logical, Unary, Literal, Grouping, Variable
from app.scanner import ValidToken, ValidTokenType
from app.stmt import Stmt, If, Print, Block, Expression, Var, While
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
        _ = self.advance()

        while not self.is_at_end():
            if self.previous().type == ValidTokenType.SEMICOLON:
                return
            match self.peek().type:
                case ValidTokenType.PRINT:
                    return

            _ = self.advance()

    def peek(self) -> ValidToken:
        return self.tokens[self.cursor]

    def is_at_end(self) -> bool:
        return self.peek().type == ValidTokenType.EOF

    def previous(self) -> ValidToken:
        return self.tokens[self.cursor - 1]

    def advance(self) -> ValidToken:
        if not self.is_at_end():
            self.cursor += 1
        return self.previous()

    def check(self, type_: ValidTokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def match(self, *types: ValidTokenType) -> bool:
        for type_ in types:
            if self.check(type_):
                _ = self.advance()
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
            if self.match(ValidTokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name = self.consume(ValidTokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(ValidTokenType.EQUAL):
            initializer = self.expression()

        self.consume(ValidTokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(ValidTokenType.IF):
            return self.if_statement()
        elif self.match(ValidTokenType.PRINT):
            return self.print_statement()
        elif self.match(ValidTokenType.WHILE):
            return self.while_statement()
        elif self.match(ValidTokenType.FOR):
            return self.for_statement()
        elif self.match(ValidTokenType.LEFT_BRACE):
            return self.block()
        else:
            return self.expression_statement()

    def block(self) -> Block:
        statements = []
        while not self.check(ValidTokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(ValidTokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(statements)

    def if_statement(self) -> Stmt:
        self.consume(ValidTokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(ValidTokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = self.statement() if self.match(ValidTokenType.ELSE) else None

        return If(condition, then_branch, else_branch)

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(ValidTokenType.SEMICOLON, "Expect ';' after value.")

        return Print(value)

    def while_statement(self) -> Stmt:
        self.consume(ValidTokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(ValidTokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return While(condition, body)

    def for_statement(self) -> Stmt:
        self.consume(ValidTokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self.match(ValidTokenType.SEMICOLON):
            initializer = None
        elif self.match(ValidTokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(ValidTokenType.SEMICOLON):
            condition = self.expression()
        self.consume(ValidTokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(ValidTokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(ValidTokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()
        if increment:
            body = Block([body, Expression(increment)])

        if condition is None:
            condition = Literal(ValidToken(ValidTokenType.TRUE, "true", None, 1))
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(ValidTokenType.SEMICOLON, "Expect ';' after expression.")

        return Expression(expr)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.or_()

        if self.match(ValidTokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def or_(self) -> Expr:
        expr = self.and_()

        while self.match(ValidTokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)

        return expr

    def and_(self) -> Expr:
        expr = self.equality()

        while self.match(ValidTokenType.AND):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)

        return expr

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
            ValidTokenType.TRUE,
            ValidTokenType.FALSE,
            ValidTokenType.NIL,
            ValidTokenType.FLOAT,
            ValidTokenType.INTEGER,
            ValidTokenType.STRING,
        ):
            return Literal(self.previous())
        if self.match(ValidTokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(ValidTokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(ValidTokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")
