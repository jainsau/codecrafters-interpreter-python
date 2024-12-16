from .expr import (
    Visitor,
    Expr,
    # Assign,
    Binary,
    # Call,
    # Get,
    Grouping,
    Literal,
    # Logical,
    # Set,
    # Super,
    # This,
    Unary,
    # Variable,
)
from typing import List


class AstPrinter(Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, *exprs: List[Expr]) -> str:
        group = [name] + [expr.accept(self) for expr in exprs]
        return f'({" ".join(group)})'

    #
    # def visit_assign_expr(self, expr: Assign) -> str:
    #     return self._parenthesize("=", expr.name.lexeme, expr.value)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    # def visit_call_expr(self, expr: Call) -> str:
    #     # TODO:
    #     return self._parenthesize("call", expr.callee, expr.arguments)
    #
    # def visit_get_expr(self, expr: Get) -> str: ...
    #
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        return expr.value.literal if expr.value.literal else expr.value.lexeme

    # def visit_logical_expr(token) -> str: ...
    #
    # def visit_set_expr(self, expr: Set) -> str: ...
    #
    # def visit_super_expr(self, expr: Super) -> str: ...
    #
    # def visit_this_expr(self, expr: This) -> str: ...

    def visit_unary_expr(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    # def visit_variable_expr(self, expr: Variable) -> str: ...
