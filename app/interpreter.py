from .expr import Visitor, Expr, Grouping, Binary, Unary, Literal
from .scanner import ValidTokenType


class Interpreter(Visitor):
    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def is_truthy(self, obj: object):
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return obj
        return True

    def visit_literal_expr(self, expr: Literal) -> object:
        if expr.value.type is ValidTokenType.INTEGER:
            return int(float(expr.value.literal))
        elif expr.value.type is ValidTokenType.FLOAT:
            return float(expr.value.literal)
        elif expr.value.type is ValidTokenType.TRUE:
            return True
        elif expr.value.type is ValidTokenType.FALSE:
            return False
        elif expr.value.type is ValidTokenType.NIL:
            return None
        return expr.value.literal if expr.value.literal else expr.value.lexeme

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case ValidTokenType.MINUS:
                return -right
            case ValidTokenType.BANG:
                return not self.is_truthy(right)

    def visit_binary_expr(self, expr: Binary) -> str:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case ValidTokenType.GREATER:
                return left > right
            case ValidTokenType.GREATER_EQUAL:
                return left >= right
            case ValidTokenType.LESS:
                return left < right
            case ValidTokenType.LESS_EQUAL:
                return left <= right
            case ValidTokenType.MINUS:
                return left - right
            case ValidTokenType.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
            case ValidTokenType.SLASH:
                return left / right
            case ValidTokenType.STAR:
                return left * right
