"""Executable entry point for fm26_auto_editor."""

from __future__ import annotations

import sys

from fm26_auto_editor.cli import main as cli_main


if __name__ == "__main__":  # pragma: no cover - entry point
    sys.exit(cli_main())
