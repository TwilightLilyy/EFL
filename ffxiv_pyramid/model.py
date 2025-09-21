"""Data models for the FFXIV football pyramid app."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Team:
    """Represents a club participating in the pyramid."""

    name: str
    location: str
    inspiration: str
    notes: Optional[str] = None


@dataclass
class Division:
    """Represents a level within the football pyramid."""

    level: int
    name: str
    short_name: Optional[str] = None
    teams: List[Team] = field(default_factory=list)


@dataclass
class Pyramid:
    """Container that describes the full pyramid."""

    title: str
    description: str
    divisions: List[Division]
    meta: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime | None = None

    def sort(self) -> None:
        """Ensure divisions are sorted by level and teams alphabetically."""

        self.divisions.sort(key=lambda d: d.level)
        for division in self.divisions:
            division.teams.sort(key=lambda t: t.name)
