from .nodes import BinaryExpr, Identifier, Node, Number
from .error import MimatError
from .lexer import Token, TokenKind


class Parser:
    def __init__(self, source: str, tokens: list[Token]) -> None:
        self.source = source
        self.tokens = tokens
        self.pos = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def error(self, message: str) -> MimatError:
        token = self.current

        return MimatError(
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
        left = self.parse_term()

        while self.current.kind in (TokenKind.PLUS, TokenKind.MINUS):
            operator = self.current.kind
            self._eat(operator)

            right = self.parse_term()

            left = BinaryExpr(
                start=left.start,
                end=right.end,
                left=left,
                operator=operator,
                right=right,
            )

        return left

    def parse_term(self) -> Node:
        left = self.parse_primary()

        while self.current.kind in (TokenKind.MULTIPLY, TokenKind.DIVIDE):
            operator = self.current.kind
            self._eat(operator)

            right = self.parse_primary()

            left = BinaryExpr(
                start=left.start,
                end=right.end,
                left=left,
                operator=operator,
                right=right,
            )

        return left

    def parse_primary(self) -> Node:
        token = self.current

        if token.kind is TokenKind.NUMBER:
            token = self._eat(TokenKind.NUMBER)
            return Number(start=token.start, end=token.end, value=int(token.value))

        if token.kind is TokenKind.IDENTIFIER:
            token = self._eat(TokenKind.IDENTIFIER)
            return Identifier(start=token.start, end=token.end, name=token.value)

        if token.kind is TokenKind.LPAREN:
            self._eat(TokenKind.LPAREN)
            node = self.parse_expression()
            closing = self._eat(TokenKind.RPAREN)

            return node

        raise self.error("Expected a number, identifier, or '('")

    def _eat(self, expected: TokenKind) -> Token:
        current = self.current

        if current.kind != expected:
            raise self.error(
                f"Expected {expected.name.lower()}, got {current.kind.name.lower()}"
            )

        self.pos += 1
        return current
