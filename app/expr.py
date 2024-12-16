from .scanner import ValidToken
from typing import List
import abc
from typing import TypeVar, Protocol


T = TypeVar("T")


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: "Visitor[T]") -> T: ...


class Visitor(Protocol[T]):
    # def visit_assign_expr(self, expr: "Assign") -> T: ...
    #
    def visit_binary_expr(self, expr: "Binary") -> T: ...

    #
    # def visit_call_expr(self, expr: "Call") -> T: ...
    #
    # def visit_get_expr(self, expr: "Get") -> T: ...
    #
    def visit_grouping_expr(self, expr: "Grouping") -> T: ...

    def visit_literal_expr(self, expr: "Literal") -> T: ...

    #
    # def visit_logical_expr(self, expr: "Logical") -> T: ...
    #
    # def visit_set_expr(self, expr: "Set") -> T: ...
    #
    # def visit_super_expr(self, expr: "Super") -> T: ...
    #
    # def visit_this_expr(self, expr: "This") -> T: ...
    #
    # def visit_unary_expr(self, expr: "Unary") -> T: ...
    #
    # def visit_variable_expr(self, expr: "Variable") -> T: ...
    #


# class Assign(Expr):
#     def __init__(self, name: ValidToken, value: Expr):
#       self.name = name
#         self.value = value
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: ValidToken, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary_expr(self)


# class Call(Expr):
#     def __init__(self, callee: Expr, paren: ValidToken, arguments: List[Expr]):
#         self.callee = callee
#         self.paren = paren
#         self.arguments = arguments
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_call_expr(self)
#
#
# class Get(Expr):
#     def __init__(self, obj: Expr, name: ValidToken):
#         self.obj = obj
#         self.name = name
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_get_expr(self)
#


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: ValidToken):
        self.value = value

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)


# class Logical(Expr):
#     def __init__(self, left: Expr, operator: ValidToken, right: Expr):
#         self.left = left
#         self.operator = operator
#         self.right = right
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_logical_expr(self)
#
#
# class Set(Expr):
#     def __init__(self, obj: Expr, name: ValidToken, value: Expr):
#         self.obj = obj
#         self.name = name
#         self.value = value
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_set_expr(self)
#
#
# class Super(Expr):
#     def __init__(self, keyword: ValidToken, method: ValidToken):
#         self.keyword = keyword
#         self.method = method
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_super_expr(self)
#
#
# class This(Expr):
#     def __init__(self, keyword: ValidToken):
#         self.keyword = keyword
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_this_expr(self)
#
#
class Unary(Expr):
    def __init__(self, operator: ValidToken, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary_expr(self)


#
#
# class Variable(Expr):
#     def __init__(self, name: ValidToken):
#         self.name = name
#
#     def accept(self, visitor: Visitor[T]) -> T:
#         return visitor.visit_variable_expr(self)
