"""Static data and helpers for FFXIV inspired content."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class Theme:
    """Represents a collection of flavour data for a pyramid theme."""

    key: str
    region_name: str
    short_prefix: str
    premier_title: str
    championship_title: str
    lower_division_title: str
    highlight: str
    locations: List[str]
    mascots: List[str]
    adjectives: List[str]
    inspirations: List[str]
    notes_templates: List[str]

    def iter_location_cycle(self) -> Iterable[str]:
        """Yield locations repeatedly, useful for ensuring enough clubs."""

        while True:
            for location in self.locations:
                yield location


THEMES: Dict[str, Theme] = {
    "eorzea": Theme(
        key="eorzea",
        region_name="Eorzean",
        short_prefix="EFL",
        premier_title="Eorzean Premier League",
        championship_title="Grand Company Championship",
        lower_division_title="City-State Division",
        highlight="The heart of the realm where Gridania, Limsa Lominsa, Ul'dah, and Ishgard compete.",
        locations=[
            "Gridania",
            "Limsa Lominsa",
            "Ul'dah",
            "Ishgard",
            "Sharlayan",
            "Radz-at-Han",
            "Mor Dhona",
            "La Noscea",
            "Coerthas",
            "Thanalan",
            "The Dravanian Forelands",
            "Lakeland",
            "Thavnair",
            "Old Sharlayan",
            "Labyrinthos",
            "Kugane",
            "Idyllshire",
            "Garlemald Reclaimed",
            "The Crystarium",
            "Old Gridania",
        ],
        mascots=[
            "Scions",
            "Seedseers",
            "Maelstrom",
            "Immortals",
            "Temple Knights",
            "Astrologians",
            "Nald'thal",
            "Azure Drakes",
            "Carbuncle",
            "Chocobos",
            "Free Paladins",
            "Gobwalkers",
            "Sky Pirates",
            "Radiant Dawn",
            "House Fortemps",
            "Conjurers",
            "Adders",
            "Flames",
            "Blades",
            "Dragoons",
        ],
        adjectives=[
            "Twin",
            "Rising",
            "Mythril",
            "Heavensward",
            "Stormborn",
            "Starlit",
            "Ruby",
            "Umbral",
            "Astral",
            "Azure",
            "Verdant",
            "Gilded",
            "Crystalline",
            "Eternal",
            "Radiant",
        ],
        inspirations=[
            "Scions of the Seventh Dawn",
            "Order of the Twin Adder",
            "Immortal Flames",
            "Maelstrom",
            "Temple Knights",
            "Ishgardian Restoration",
            "Crystarium Guard",
            "Students of Baldesion",
            "Radz-at-Han alchemists",
            "Sharlayan Forum",
            "Bozjan Resistance",
        ],
        notes_templates=[
            "Backed by the {inspiration} from {location}.",
            "Founded by veterans of the {inspiration}.",
            "Club culture steeped in {inspiration} tradition.",
            "Hails from {location} with {inspiration} influence.",
        ],
    ),
    "far_east": Theme(
        key="far_east",
        region_name="Far Eastern",
        short_prefix="FEF",
        premier_title="Kugane Premier Division",
        championship_title="Hingan Championship",
        lower_division_title="Eastern League",
        highlight="The trading ports of Kugane, the rebel lands of Doma, and the wandering Steppe tribes collide.",
        locations=[
            "Kugane",
            "Doma",
            "Yanxia",
            "The Azim Steppe",
            "Hingashi",
            "Sui-no-Sato",
            "The Ruby Sea",
            "Isari",
            "Namai",
            "Tsurumi",
            "Shisui of the Violet Tides",
            "Reunion",
            "Tamamizu",
            "Shirogane",
            "Onokoro",
            "Seigetsu",
        ],
        mascots=[
            "Sekiseigumi",
            "Raen",
            "Xaela",
            "Ruby Ronin",
            "Steppe Riders",
            "Doman Clans",
            "Geiko",
            "Raijin",
            "Komainu",
            "Crimson Lancers",
            "Blue Oni",
            "Sea Wolves",
            "Tengu",
            "Moonlit Ronin",
            "Skyfarers",
        ],
        adjectives=[
            "Blossom",
            "Moonlit",
            "Stormjade",
            "Tempest",
            "Crimson",
            "Azure",
            "Sakura",
            "Silver",
            "Verdant",
            "Dragon",
        ],
        inspirations=[
            "Sekiseigumi",
            "House of the Fierce",
            "Confederacy",
            "Doman Liberation Front",
            "Mol Warriors",
            "Seiryu Temple",
            "Tales of the Ruby Princess",
        ],
        notes_templates=[
            "Backed by the {inspiration} from {location}.",
            "Combines tactics from the {inspiration} with Far Eastern flair.",
            "Favoured by sailors of the {inspiration}.",
        ],
    ),
    "garlemald": Theme(
        key="garlemald",
        region_name="Imperial",
        short_prefix="IGL",
        premier_title="Imperial Supremacy League",
        championship_title="Praetoriate Championship",
        lower_division_title="Legion Divisions",
        highlight="Reformed Garlean legions and liberated provinces contest the imperial title.",
        locations=[
            "Garlemald",
            "Bozja",
            "Werlyt",
            "Dalmasca",
            "Ala Mhigo",
            "Terncliff",
            "Paglth'an",
            "Corvos",
            "Iskaal",
            "Locus Amoenus",
            "Porta Praetoria",
            "Tertium",
            "Zadnor",
        ],
        mascots=[
            "Magitek",
            "Legati",
            "Centurions",
            "Ceruleum",
            "Gunblades",
            "Dreadnaughts",
            "Praetorians",
            "Machina",
            "Imperial Fangs",
            "Ala Mhigan Shields",
            "Resistance",
        ],
        adjectives=[
            "Adamant",
            "Iron",
            "Cerulean",
            "Imperial",
            "Reborn",
            "Resolute",
            "Steel",
            "Vanguard",
        ],
        inspirations=[
            "IVth Legion",
            "Bozjan Resistance",
            "Werlyt Rebellion",
            "Dalmascan Royalists",
            "Ala Mhigan Monks",
            "Corvos Insurgents",
        ],
        notes_templates=[
            "Former {inspiration} unit now focused on footballing glory.",
            "Uses magitek support from {location}.",
            "Celebrates {inspiration} heritage in every match.",
        ],
    ),
}


def get_theme(key: str) -> Theme:
    """Retrieve a theme by key, raising a helpful error if missing."""

    lowered = key.lower().replace("-", "_")
    if lowered not in THEMES:
        available = ", ".join(sorted(THEMES))
        raise KeyError(f"Unknown theme '{key}'. Available themes: {available}")
    return THEMES[lowered]
