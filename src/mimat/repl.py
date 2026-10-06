from __future__ import annotations
import importlib.metadata

from .error import MimatError

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

        try:
            tokens = Lexer(src).tokenize()
        except MimatError as exc:
            print(f"error: {exc}")
            continue

        __import__("pprint").pprint(tokens)


def main() -> None:
    """main entry point for mimat cmd."""
    try:
        run()
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
