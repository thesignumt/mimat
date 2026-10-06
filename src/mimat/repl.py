from __future__ import annotations

import sys
from .lexer import Lexer, TokenKind


def run() -> None:
    print("mimat")

    while True:
        try:
            src = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("bye!")
            break

        tokens = Lexer(src).tokenize()
        t0 = tokens[0]
        if t0.kind == TokenKind.ERROR:
            print(t0.value)
        else:
            __import__("pprint").pprint(tokens)


def main() -> None:
    """main entry point for mimat cmd."""
    try:
        run()
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
