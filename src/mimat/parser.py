from .nodes import BinaryExpr, Identifier, Node, Number
from .error import ParserError
from .lexer import Token, TokenKind


class Parser:
    def __init__(self, source: str, tokens: list[Token]) -> None:
        self.source = source
        self.tokens = tokens
        self.pos = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def error(self, message: str) -> ParserError:
        token = self.current

        return ParserError(
            message,
            source=self.source,
            start=token.start,
            end=token.end,
        )

    def parse(self) -> Node:
        node = self.parse_expression()
        self._eat(TokenKind.EOF)
        return node

    def parse_expression(self) -> Node:
        left = self.parse_value()

        while self.current.kind == TokenKind.PLUS:
            self._eat(TokenKind.PLUS)
            right = self.parse_value()

            left = BinaryExpr(
                start=left.start,
                end=right.end,
                left=left,
                operator=TokenKind.PLUS,
                right=right,
            )

        return left

    def parse_value(self) -> Node:
        current = self.current

        if current.kind == TokenKind.NUMBER:
            token = self._eat(TokenKind.NUMBER)

            return Number(
                start=token.start,
                end=token.end,
                value=int(token.value),
            )

        if current.kind == TokenKind.IDENTIFIER:
            token = self._eat(TokenKind.IDENTIFIER)

            return Identifier(
                start=token.start,
                end=token.end,
                name=token.value,
            )

        raise self.error("Expected a value")

    def _eat(self, expected: TokenKind) -> Token:
        current = self.current

        if current.kind != expected:
            raise self.error(
                f"Expected {expected.name.lower()}, got {current.kind.name.lower()}"
            )

        self.pos += 1
        return current
