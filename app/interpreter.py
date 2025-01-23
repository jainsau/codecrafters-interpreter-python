from app.expr import (
    ExprVisitor,
    Expr,
    Assign,
    Grouping,
    Binary,
    Unary,
    Literal,
    Variable,
)
from app.stmt import StmtVisitor, Stmt, Expression, Print, Var
from app.scanner import ValidToken, ValidTokenType
from app.error import RuntimeError_
from app.environment import Environment
from app import lox
from typing import List


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self._environment = Environment()

    def interpret_expr(self, expr: Expr) -> None:
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeError_ as error:
            lox.Lox.runtime_error(error)

    def interpret(self, statements: List[Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError_ as error:
            lox.Lox.runtime_error(error)

    def stringify(self, value: object) -> str:
        if value is None:
            return "nil"
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif type(value) is float:
            return f"{int(value) if int(value) == value else value}"
        else:
            return value

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def is_truthy(self, obj: object):
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return obj
        return True

    def is_number(self, value: object) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False
        return True

    def check_number_operand(self, operator: ValidToken, operand: object) -> None:
        if self.is_number(operand):
            return
        raise RuntimeError_(operator, "Operand must be a number.")

    def check_number_operands(
        self, operator: ValidToken, left: object, right: object
    ) -> None:
        if self.is_number(left) and self.is_number(right):
            return
        raise RuntimeError_(operator, "Operands must be numbers.")

    def is_equal(self, a: object, b: object) -> bool:
        if (a is None) ^ (b is None):
            return True

        return a == b

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt: Var) -> None:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)

    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value

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
        if expr.value.literal is not None:
            return expr.value.literal
        else:
            return expr.value.lexeme

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case ValidTokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case ValidTokenType.BANG:
                return not self.is_truthy(right)

    def visit_variable_expr(self, expr: Variable) -> object:
        return self._environment.get(expr.name)

    def visit_binary_expr(self, expr: Binary) -> str:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case ValidTokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case ValidTokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case ValidTokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case ValidTokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case ValidTokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case ValidTokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case ValidTokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case ValidTokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                self.check_number_operands(expr.operator, left, right)
                return left + right
            case ValidTokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            case ValidTokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right
