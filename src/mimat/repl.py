from __future__ import annotations
import importlib.metadata
from icecream import ic
import sys

from .error import MimatError
from .lexer import Lexer, TokenKind
from .parser import Parser
from .evaluator import evaluate


MIMAT_VER = importlib.metadata.version("mimat")


def run_mimat() -> None:
    print(f"mimat v{MIMAT_VER}")

    while True:
        try:
            src = input("mimat> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if src[-1] == "\x04":
            break

        if not src:
            print()
            continue

        try:
            tokens = Lexer(src).tokenize()
            node = Parser(src, tokens).parse()
            result = evaluate(node)
        except MimatError as exc:
            print(f"error: {exc}")
            continue

        ic(tokens[:-1], node, result)

    print("\nbye!")


def main() -> None:
    """main entry point for mimat cmd."""
    try:
        run_mimat()
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
