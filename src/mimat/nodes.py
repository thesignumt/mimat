from dataclasses import dataclass
from .lexer import TokenKind


@dataclass(frozen=True)
class Node:
    start: int
    end: int


@dataclass(frozen=True)
class Number(Node):
    value: int


@dataclass(frozen=True)
class Identifier(Node):
    name: str


@dataclass(frozen=True)
class BinaryExpr(Node):
    left: Node
    operator: TokenKind
    right: Node
