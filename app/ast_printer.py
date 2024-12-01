from .expr import (
    Visitor,
    Expr,
    Grouping,
    Literal,
)
from typing import List


class AstPrinter(Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, *exprs: List[Expr]) -> str:
        group = [name] + [expr.accept(self) for expr in exprs]
        return f'({" ".join(group)})'

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        return expr.value if expr.value else "nil"
