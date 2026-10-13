from __future__ import annotations
import importlib.metadata
from icecream import ic
import sys
import argparse

from .error import MimatError
from .lexer import Lexer, TokenKind
from .parser import Parser
from .evaluator import evaluate


__version__ = importlib.metadata.version("mimat")


def run_mimat(*, verbose: bool | None = False) -> None:
    print(f"mimat v{__version__}")

    while True:
        try:
            src = input("mimat> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not src:
            print()
            continue

        try:
            tokens = Lexer(src).tokenize()
            if verbose:
                ic(tokens[:-1])

            node = Parser(src, tokens).parse()
            if verbose:
                ic(node)

            result = evaluate(node)
        except MimatError as exc:
            print(f"error: {exc}")
            continue

        print(result)

    print("\nbye!")


def main() -> None:
    """main entry point for mimat cmd."""
    parser = argparse.ArgumentParser(prog="mimat")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s v{__version__}"
    )

    args = parser.parse_args()

    try:
        run_mimat(verbose=args.verbose)
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
