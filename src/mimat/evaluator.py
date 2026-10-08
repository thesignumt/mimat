from .nodes import Node, Number, Identifier, BinaryExpr
from .lexer import TokenKind
from .error import MimatError


def evaluate(node):
    if isinstance(node, Number):
        return node.value

    if isinstance(node, Identifier):
        raise MimatError("TODO: variables")

    if isinstance(node, BinaryExpr):
        left = evaluate(node.left)
        right = evaluate(node.right)

        if node.operator is TokenKind.PLUS:
            return left + right

        raise MimatError("unknown operator")

    raise MimatError("unknown node")
