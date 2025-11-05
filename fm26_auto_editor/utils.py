"""Utility helpers for :mod:`fm26_auto_editor`.

This module centralises functionality that is reused across the package, such as
logging configuration, string normalisation helpers, and stable random number
generation for change records.
"""

from __future__ import annotations

import hashlib
import logging
import sys
from typing import Optional

_LOGGER_INITIALISED: bool = False


def configure_logging(verbosity: int = 0) -> None:
    """Configure logging for the application.

    Parameters
    ----------
    verbosity:
        Verbosity level from the command line. ``0`` configures :mod:`logging`
        at :data:`logging.INFO`; higher values increase verbosity to
        :data:`logging.DEBUG`.
    """

    global _LOGGER_INITIALISED

    if _LOGGER_INITIALISED:
        logging.getLogger(__name__).debug("Logging already initialised")
        return

    level = logging.DEBUG if verbosity > 0 else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    _LOGGER_INITIALISED = True


def normalise_optional(value: Optional[str]) -> Optional[str]:
    """Return the stripped value or ``None`` if the input is empty."""

    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def parse_int(value: Optional[str]) -> Optional[int]:
    """Parse *value* into an integer, returning ``None`` on failure."""

    if value is None:
        return None
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None


def make_db_random_id(uid: int, property_id: int, new_value: str | int) -> int:
    """Generate a stable pseudo-random integer for change records.

    The Football Manager editor expects each record to include a ``db_random_id``
    value. The editor typically provides this value automatically, but when
    generating records programmatically we mimic the behaviour by hashing the
    tuple ``(uid, property_id, new_value)`` using SHA-1 and converting the first
    four bytes of the digest to a positive integer.
    """

    seed = f"{uid}-{property_id}-{new_value}".encode("utf-8")
    digest = hashlib.sha1(seed).digest()
    return int.from_bytes(digest[:4], byteorder="big", signed=False)


__all__ = [
    "configure_logging",
    "normalise_optional",
    "parse_int",
    "make_db_random_id",
]
