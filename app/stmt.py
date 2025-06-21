import abc
from typing import Protocol, TypeVar, Optional

from .expr import Expr
from .scanner import ValidToken

T = TypeVar("T")


class StmtVisitor(Protocol[T]):
    def visit_print_stmt(self, stmt: "Print") -> T: ...

    def visit_block_stmt(self, stmt: "Block") -> T: ...

    def visit_if_stmt(self, stmt: "If") -> T: ...

    def visit_expression_stmt(self, stmt: "Expression") -> T: ...

    def visit_var_stmt(self, stmt: "Var") -> T: ...


class Stmt(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: "StmtVisitor[T]") -> T: ...


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_print_stmt(self)


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_block_stmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Optional[Stmt]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_if_stmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_expression_stmt(self)


class Var(Stmt):
    def __init__(self, name: ValidToken, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor[T]) -> T:
        return visitor.visit_var_stmt(self)
