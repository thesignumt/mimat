from dataclasses import dataclass
from fractions import Fraction
from .lexer import TokenKind


@dataclass(frozen=True)
class Node:
    start: int
    end: int


@dataclass(frozen=True)
class Number(Node):
    value: Fraction


@dataclass(frozen=True)
class Identifier(Node):
    name: str


@dataclass(frozen=True)
class BinaryExpr(Node):
    left: Node
    operator: TokenKind
    right: Node


@dataclass(frozen=True)
class UnaryExpr(Node):
    operator: TokenKind
    operand: Node
