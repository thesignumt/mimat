from dataclasses import dataclass
from enum import Enum, auto

from .error import MimatError


class TokenKind(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: str
    start: int
    end: int


class Lexer:
    SINGLE_CHAR_TOKENS = {
        "+": TokenKind.PLUS,
        "-": TokenKind.MINUS,
        "*": TokenKind.MULTIPLY,
        "/": TokenKind.DIVIDE,
        "(": TokenKind.LPAREN,
        ")": TokenKind.RPAREN,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0

    def error(self, message: str) -> MimatError:
        return MimatError(
            message,
            source=self.source,
            start=self.pos,
            end=self.pos + 1,
        )

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while self.pos < len(self.source):
            c = self._peek()

            if c.isspace():
                self._advance()
                continue

            if c.isdecimal():
                tokens.append(self.read_number())
                continue

            if (c.isascii() and c.isalpha()) or c == "\\":
                tokens.append(self.read_identifier())
                continue

            kind = self.SINGLE_CHAR_TOKENS.get(c)
            if kind is not None:
                tokens.append(self._single_char(kind))
                continue

            raise self.error(f"Unexpected character {c!r}")

        tokens.append(Token(TokenKind.EOF, "", self.pos, self.pos))

        return tokens

    def read_number(self) -> Token:
        start = self.pos

        while self.pos < len(self.source) and self._peek().isdecimal():
            self._advance()

        return Token(
            TokenKind.NUMBER,
            self.source[start : self.pos],
            start,
            self.pos,
        )

    def read_identifier(self) -> Token:
        start = self.pos

        if self._peek() == "\\":
            self._advance()

            if self.pos >= len(self.source):
                raise self.error("Expected identifier after '\\'")

            if not self._peek().isascii() or not self._peek().isalpha():
                raise self.error("Expected letter after '\\'")

        self._advance()

        while (
            self.pos < len(self.source)
            and self._peek().isascii()
            and self._peek().isalpha()
        ):
            self._advance()

        return Token(
            TokenKind.IDENTIFIER,
            self.source[start : self.pos],
            start,
            self.pos,
        )

    def _peek(self) -> str:
        return self.source[self.pos]

    def _advance(self) -> str:
        c = self.source[self.pos]
        self.pos += 1
        return c

    def _single_char(self, kind: TokenKind) -> Token:
        start = self.pos
        value = self._advance()

        return Token(kind, value, start, self.pos)
