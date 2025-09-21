"""Serialization helpers for pyramids."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict

from .model import Division, Pyramid, Team


def pyramid_to_dict(pyramid: Pyramid) -> Dict[str, Any]:
    """Convert a :class:`Pyramid` into a JSON serialisable dict."""

    return {
        "title": pyramid.title,
        "description": pyramid.description,
        "generated_at": pyramid.generated_at.isoformat() if pyramid.generated_at else None,
        "meta": pyramid.meta,
        "divisions": [
            {
                "level": division.level,
                "name": division.name,
                "short_name": division.short_name,
                "teams": [
                    {
                        "name": team.name,
                        "location": team.location,
                        "inspiration": team.inspiration,
                        "notes": team.notes,
                    }
                    for team in division.teams
                ],
            }
            for division in pyramid.divisions
        ],
    }


def dict_to_pyramid(data: Dict[str, Any]) -> Pyramid:
    """Reconstruct a :class:`Pyramid` from the serialised form."""

    divisions = []
    for division_data in data.get("divisions", []):
        teams = [
            Team(
                name=team_data["name"],
                location=team_data.get("location", ""),
                inspiration=team_data.get("inspiration", ""),
                notes=team_data.get("notes"),
            )
            for team_data in division_data.get("teams", [])
        ]
        divisions.append(
            Division(
                level=int(division_data["level"]),
                name=division_data["name"],
                short_name=division_data.get("short_name"),
                teams=teams,
            )
        )
    generated_at = data.get("generated_at")
    if generated_at:
        generated_at = datetime.fromisoformat(generated_at)
    else:
        generated_at = None

    pyramid = Pyramid(
        title=data.get("title", "Unnamed Pyramid"),
        description=data.get("description", ""),
        divisions=divisions,
        meta=data.get("meta", {}),
        generated_at=generated_at,
    )
    pyramid.sort()
    return pyramid


def save_pyramid(pyramid: Pyramid, path: str | Path) -> Path:
    """Serialise the pyramid to JSON on disk."""

    target = Path(path)
    if target.suffix.lower() != ".json":
        raise ValueError("The app currently writes JSON. Use a .json file extension.")
    payload = pyramid_to_dict(pyramid)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def load_pyramid(path: str | Path) -> Pyramid:
    """Load a pyramid definition from disk."""

    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Pyramid file not found: {source}")
    data = json.loads(source.read_text(encoding="utf-8"))
    return dict_to_pyramid(data)
