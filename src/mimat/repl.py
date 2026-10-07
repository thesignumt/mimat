from __future__ import annotations
import importlib.metadata
from icecream import ic


MIMAT_VER = importlib.metadata.version("mimat")

import sys
from .error import MimatError
from .lexer import Lexer, TokenKind
from .parser import Parser


def run() -> None:
    print(f"mimat v{MIMAT_VER}")

    while True:
        try:
            src = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye!")
            break

        if not src:
            print()
            continue

        try:
            tokens = Lexer(src).tokenize()
            ast = Parser(src, tokens).parse()
        except MimatError as exc:
            print(f"error: {exc}")
            continue

        ic(tokens[:-1], ast)


def main() -> None:
    """main entry point for mimat cmd."""
    try:
        run()
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
