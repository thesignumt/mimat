from __future__ import annotations
import importlib.metadata

MIMAT_VER = importlib.metadata.version("mimat")

import sys
from .lexer import Lexer, TokenKind


def run() -> None:
    print(f"mimat v{MIMAT_VER}")

    while True:
        try:
            src = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nbye!")
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
