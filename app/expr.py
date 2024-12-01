import abc
from typing import TypeVar, Protocol


T = TypeVar("T")


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: "Visitor[T]") -> T: ...


class Visitor(Protocol[T]):
    def visit_grouping_expr(self, expr: "Grouping") -> T: ...

    def visit_literal_expr(self, expr: "Literal") -> T: ...


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)
