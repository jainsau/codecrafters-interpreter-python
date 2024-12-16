from .expr import Visitor, Expr, Literal
from .scanner import ValidTokenType


class Interpreter(Visitor):
    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visit_literal_expr(self, expr: Literal) -> object:
        if expr.value.type is ValidTokenType.INTEGER:
            return int(float(expr.value.literal))
        return expr.value.literal if expr.value.literal else expr.value.lexeme
