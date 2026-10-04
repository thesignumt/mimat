from __future__ import annotations

import sys


def run() -> None:
    print("mimat")

    while True:
        try:
            expression = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("bye!")
            break


def main() -> None:
    """main entry point for mimat cmd."""
    try:
        run()
    except Exception as exc:
        print(f"mimat: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
