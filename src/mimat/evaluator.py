__all__ = ["evaluate"]

from .nodes import Node, Number, Identifier, BinaryExpr
from .lexer import TokenKind
from .error import MimatError

OPERATORS = {
    TokenKind.PLUS: lambda a, b: a + b,
    TokenKind.MINUS: lambda a, b: a - b,
}


def evaluate(node):
    if isinstance(node, Number):
        return node.value

    if isinstance(node, Identifier):
        raise MimatError("TODO: variables")

    if isinstance(node, BinaryExpr):
        left = evaluate(node.left)
        right = evaluate(node.right)

        operation = OPERATORS.get(node.operator)

        if operation is None:
            raise MimatError("unknown operator")

        return operation(left, right)

    raise MimatError("unknown node")
