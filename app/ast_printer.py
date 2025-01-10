from app.expr import (
    ExprVisitor,
    Expr,
    Binary,
    Grouping,
    Literal,
    Unary,
)
from typing import List


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, *exprs: List[Expr]) -> str:
        group = [name] + [expr.accept(self) for expr in exprs]
        return f'({" ".join(group)})'

    def visit_binary_expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        return expr.value.literal if expr.value.literal else expr.value.lexeme

    def visit_unary_expr(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)
