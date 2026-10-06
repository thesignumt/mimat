from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()

    ERROR = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: str


def err(msg: str) -> Token:
    return Token(TokenKind.ERROR, msg)


class Lexer:
    def __init__(self, source: str) -> None:
        self.src = source
        self.pos = 0

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while self.pos < len(self.src):
            c = self._peek()

            if c.isspace():
                self._advance()
                continue

            if c.isdecimal():
                tokens.append(self.read_number())
                continue

            if c.isascii() and c.isalpha():  # only allow A-Z/a-z
                tokens.append(self.read_identifier())
                continue

            if c == "+":
                tokens.append(self._single_char(TokenKind.PLUS))
                continue

            return [
                err(
                    f"unexpected {c!r} at position {self.pos}",
                )
            ]

        return tokens

    def read_number(self) -> Token:
        start = self.pos

        while self.pos < len(self.src) and self._peek().isdecimal():
            self._advance()

        return Token(TokenKind.NUMBER, self.src[start : self.pos])

    def read_identifier(self) -> Token:
        start = self.pos

        while (
            self.pos < len(self.src)
            and self._peek().isascii()
            and self._peek().isalpha()
        ):
            self._advance()

        return Token(TokenKind.IDENTIFIER, self.src[start : self.pos])

    def _peek(self) -> str:
        return self.src[self.pos]

    def _advance(self) -> str:
        c = self.src[self.pos]
        self.pos += 1
        return c

    def _single_char(self, kind: TokenKind) -> Token:
        return Token(kind, self._advance())
