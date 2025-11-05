"""Module entry point for ``python -m fm26_auto_editor``."""

from __future__ import annotations

import sys

from .cli import main


def run() -> None:
    """Execute the command line interface and exit with its status code."""

    sys.exit(main())


if __name__ == "__main__":  # pragma: no cover - entry point
    run()
