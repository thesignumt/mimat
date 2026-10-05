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
        if tokens[0].kind != TokenKind.ERROR:
            __import__("pprint").pprint(tokens)


def main() -> None:
    """main entry point for mimat cmd."""
    try:
        run()
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
