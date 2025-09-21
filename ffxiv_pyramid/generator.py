"""Tools to create themed football pyramids."""
from __future__ import annotations

from datetime import datetime
import random
from typing import List, Sequence

from .data import Theme, get_theme
from .model import Division, Pyramid, Team
_EXTRA_TEAM_SUFFIXES = ["FC", "United", "Wanderers", "Rovers", "Dynasts", "Guard", "Club"]


def _roman(number: int) -> str:
    """Convert an integer into a Roman numeral."""

    numerals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    result = []
    remaining = number
    for value, numeral in numerals:
        while remaining >= value:
            result.append(numeral)
            remaining -= value
    return "".join(result) if result else "I"


def _division_name(theme: Theme, level: int, total_levels: int, custom: Sequence[str] | None = None) -> str:
    if custom and len(custom) >= level:
        return custom[level - 1]
    if level == 1:
        return theme.premier_title
    if level == 2:
        return theme.championship_title
    suffix = theme.lower_division_title
    roman_value = _roman(level - 2)
    return f"{theme.region_name} {suffix} {roman_value}"


def _short_name(theme: Theme, level: int) -> str:
    return f"{theme.short_prefix} L{level}"


def _build_team(theme: Theme, rng: random.Random, used_names: set[str]) -> Team:
    location = rng.choice(theme.locations)
    mascot = rng.choice(theme.mascots)
    adjective = rng.choice(theme.adjectives)
    base_name = f"{location} {mascot}" if rng.random() < 0.55 else f"{location} {adjective} {mascot}"
    name = base_name
    while name in used_names:
        suffix = rng.choice(_EXTRA_TEAM_SUFFIXES)
        name = f"{base_name} {suffix}"
    used_names.add(name)
    inspiration = rng.choice(theme.inspirations)
    notes_template = rng.choice(theme.notes_templates)
    notes = notes_template.format(inspiration=inspiration, location=location)
    return Team(name=name, location=location, inspiration=inspiration, notes=notes)


def _build_division(
    theme: Theme,
    level: int,
    team_count: int,
    total_levels: int,
    rng: random.Random,
    used_names: set[str],
    custom_names: Sequence[str] | None = None,
) -> Division:
    name = _division_name(theme, level, total_levels, custom=custom_names)
    short_name = _short_name(theme, level)
    teams = [_build_team(theme, rng, used_names) for _ in range(team_count)]
    return Division(level=level, name=name, short_name=short_name, teams=teams)


def generate_pyramid(
    level_sizes: Sequence[int],
    *,
    theme: str = "eorzea",
    seed: int | None = None,
    title: str | None = None,
    description: str | None = None,
    custom_division_names: Sequence[str] | None = None,
    extra_meta: dict | None = None,
) -> Pyramid:
    """Create a fresh pyramid using the supplied options."""

    if not level_sizes:
        raise ValueError("At least one level size is required to generate a pyramid.")

    theme_obj = get_theme(theme)
    rng = random.Random(seed)
    used_names: set[str] = set()

    divisions: List[Division] = []
    total_levels = len(level_sizes)
    for idx, team_count in enumerate(level_sizes, start=1):
        division = _build_division(
            theme_obj,
            level=idx,
            team_count=team_count,
            total_levels=total_levels,
            rng=rng,
            used_names=used_names,
            custom_names=custom_division_names,
        )
        divisions.append(division)

    pyramid_title = title or f"{theme_obj.region_name} Football Pyramid"
    pyramid_description = description or theme_obj.highlight

    meta = {
        "theme": theme_obj.key,
        "seed": seed,
        "levels": list(level_sizes),
        "short_prefix": theme_obj.short_prefix,
        "generated_using": "ffxiv_pyramid",
    }
    if custom_division_names:
        meta["custom_division_names"] = list(custom_division_names)
    if extra_meta:
        meta.update(extra_meta)

    pyramid = Pyramid(
        title=pyramid_title,
        description=pyramid_description,
        divisions=divisions,
        meta=meta,
        generated_at=datetime.utcnow(),
    )
    pyramid.sort()
    return pyramid
