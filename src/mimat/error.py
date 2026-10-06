from __future__ import annotations


class MimatError(Exception):
    def __init__(
        self,
        message: str,
        *,
        source: str | None = None,
        start: int | None = None,
        end: int | None = None,
    ):
        super().__init__(message)
        self.source = source
        self.start = start
        self.end = end

    def __str__(self) -> str:
        message = super().__str__()

        if self.source is None or self.start is None or self.end is None:
            return message

        width = max(1, self.end - self.start)

        return f"{message}\n\n  {self.source}\n  {' ' * self.start}{'^' * width}"


class LexerError(MimatError): ...


class ParserError(MimatError): ...


class MimatRuntimeError(MimatError): ...
