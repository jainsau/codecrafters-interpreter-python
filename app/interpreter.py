from .expr import Visitor, Expr, Grouping, Binary, Unary, Literal


class Interpreter(Visitor):
    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value
