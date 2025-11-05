"""Database table type and property ID constants for Football Manager 2026.

The numeric identifiers defined here mirror those used by the Football Manager
Pre-Game Editor when exporting XML data files. Keeping them in a dedicated
module makes it easier to reference and extend as additional object types or
properties are supported by :mod:`fm26_auto_editor`.
"""

from __future__ import annotations

# Database table types -------------------------------------------------------

# NOTE: Table type identifiers are determined by Sports Interactive's internal
# schema. They are included here verbatim so that the editor can target the
# correct table within the FM database when creating change records.
TABLE_CITY: int = 2
TABLE_CLUB: int = 3
TABLE_CONTINENT: int = 5
TABLE_MEDIA: int = 7
TABLE_NATION: int = 10
TABLE_COMPETITION: int = 25
TABLE_REGION: int = 27

# Club property identifiers --------------------------------------------------

# These property IDs correspond to specific club fields. Only a subset that is
# required for the initial version of the tool is included.
PROP_CLUB_LONG_NAME: int = 1_131_307_373
PROP_CLUB_SHORT_NAME: int = 1_131_638_381
PROP_CLUB_ABBR3_A: int = 1_131_640_942
PROP_CLUB_ABBR3_B: int = 1_131_164_526
PROP_CLUB_ABBR2: int = 1_130_443_630
PROP_CLUB_TAG: int = 1_413_703_796
PROP_CLUB_VAL1: int = 1_130_586_721
PROP_CLUB_VAL2: int = 1_131_700_853
PROP_CLUB_VAL3: int = 1_131_572_578

# Competition property identifiers ------------------------------------------
PROP_COMP_FULL_NAME: int = 1_668_178_285
PROP_COMP_ALT_NAME: int = 1_668_509_293
PROP_COMP_SHORT_NAME: int = 1_664_314_478

# Nation property identifiers ------------------------------------------------
PROP_NATION_NAME: int = 1_315_856_749
PROP_NATION_SHORT: int = 1_316_187_757
PROP_NATION_CODE3: int = 1_311_992_942
PROP_NATION_ADJ: int = 1_315_861_625

# Continent property identifiers --------------------------------------------
PROP_CONT_NAME: int = 1_131_307_373

__all__ = [
    "TABLE_CITY",
    "TABLE_CLUB",
    "TABLE_CONTINENT",
    "TABLE_MEDIA",
    "TABLE_NATION",
    "TABLE_COMPETITION",
    "TABLE_REGION",
    "PROP_CLUB_LONG_NAME",
    "PROP_CLUB_SHORT_NAME",
    "PROP_CLUB_ABBR3_A",
    "PROP_CLUB_ABBR3_B",
    "PROP_CLUB_ABBR2",
    "PROP_CLUB_TAG",
    "PROP_CLUB_VAL1",
    "PROP_CLUB_VAL2",
    "PROP_CLUB_VAL3",
    "PROP_COMP_FULL_NAME",
    "PROP_COMP_ALT_NAME",
    "PROP_COMP_SHORT_NAME",
    "PROP_NATION_NAME",
    "PROP_NATION_SHORT",
    "PROP_NATION_CODE3",
    "PROP_NATION_ADJ",
    "PROP_CONT_NAME",
]
