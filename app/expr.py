import abc
from typing import Protocol, TypeVar

from .scanner import ValidToken

T = TypeVar("T")


class ExprVisitor(Protocol[T]):
    def visit_assign_expr(self, expr: "Assign") -> T: ...

    def visit_binary_expr(self, expr: "Binary") -> T: ...

    def visit_grouping_expr(self, expr: "Grouping") -> T: ...

    def visit_literal_expr(self, expr: "Literal") -> T: ...

    def visit_logical_expr(self, expr: "Logical") -> T: ...

    def visit_unary_expr(self, expr: "Unary") -> T: ...

    def visit_variable_expr(self, expr: "Variable") -> T: ...


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: "ExprVisitor[T]") -> T: ...


class Assign(Expr):
    def __init__(self, name: ValidToken, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: ValidToken, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: ValidToken):
        self.value = value

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    def __init__(
        self,
        left: Expr,
        operator: ValidToken,
        right: Expr,
    ):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_logical_expr(self)


class Unary(Expr):
    def __init__(self, operator: ValidToken, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    def __init__(self, name: ValidToken):
        self.name = name

    def accept(self, visitor: ExprVisitor[T]) -> T:
        return visitor.visit_variable_expr(self)
