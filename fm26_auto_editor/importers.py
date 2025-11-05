"""CSV importers that translate rows into Football Manager change records."""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Iterable, List, Tuple
from xml.etree import ElementTree as ET

from . import constants
from .changes import add_int_change, add_string_change
from .utils import normalise_optional, parse_int

LOGGER = logging.getLogger(__name__)

Row = Tuple[int, dict[str, str]]


def _iter_rows(csv_path: Path) -> Iterable[Row]:
    """Yield ``(line_number, row_dict)`` tuples for each row in *csv_path*."""

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=2):
            LOGGER.debug("Processing row %s from %s", index, csv_path)
            yield index, row


def _load_rows(csv_path: str) -> List[Row]:
    path = Path(csv_path)
    if not path.exists():
        LOGGER.error("CSV file not found: %s", csv_path)
        return []
    return list(_iter_rows(path))


def apply_competition_changes_from_csv(db_changes: ET.Element, version: int, csv_path: str) -> int:
    """Apply competition changes from *csv_path* and return the number of edits."""

    count = 0
    for line_no, row in _load_rows(csv_path):
        uid = parse_int(row.get("competition_uid"))
        if uid is None:
            LOGGER.error("Invalid or missing competition_uid on line %s in %s", line_no, csv_path)
            continue
        full_name = normalise_optional(row.get("full_name"))
        alt_name = normalise_optional(row.get("alt_name"))
        short_name = normalise_optional(row.get("short_name"))

        if full_name:
            add_string_change(
                db_changes,
                constants.TABLE_COMPETITION,
                uid,
                constants.PROP_COMP_FULL_NAME,
                full_name,
                version,
            )
            count += 1
            alt_for_property = alt_name or full_name
            add_string_change(
                db_changes,
                constants.TABLE_COMPETITION,
                uid,
                constants.PROP_COMP_ALT_NAME,
                alt_for_property,
                version,
            )
            count += 1
        elif alt_name:
            add_string_change(
                db_changes,
                constants.TABLE_COMPETITION,
                uid,
                constants.PROP_COMP_ALT_NAME,
                alt_name,
                version,
            )
            count += 1

        if short_name:
            add_string_change(
                db_changes,
                constants.TABLE_COMPETITION,
                uid,
                constants.PROP_COMP_SHORT_NAME,
                short_name,
                version,
            )
            count += 1

    LOGGER.info("Applied %s competition changes from %s", count, csv_path)
    return count


def apply_club_changes_from_csv(db_changes: ET.Element, version: int, csv_path: str) -> int:
    """Apply club changes from *csv_path* and return the number of edits."""

    count = 0
    for line_no, row in _load_rows(csv_path):
        uid = parse_int(row.get("club_uid"))
        if uid is None:
            LOGGER.error("Invalid or missing club_uid on line %s in %s", line_no, csv_path)
            continue

        long_name = normalise_optional(row.get("long_name"))
        short_name = normalise_optional(row.get("short_name"))
        short_code3 = normalise_optional(row.get("short_code3"))
        short_code2 = normalise_optional(row.get("short_code2"))
        tag = normalise_optional(row.get("tag"))
        val1 = parse_int(row.get("val1"))
        val2 = parse_int(row.get("val2"))
        val3 = parse_int(row.get("val3"))

        if long_name:
            add_string_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_LONG_NAME,
                long_name,
                version,
            )
            count += 1
        if short_name:
            add_string_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_SHORT_NAME,
                short_name,
                version,
            )
            count += 1
        if short_code3:
            add_string_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_ABBR3_A,
                short_code3,
                version,
            )
            add_string_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_ABBR3_B,
                short_code3,
                version,
            )
            count += 2
        if short_code2:
            add_string_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_ABBR2,
                short_code2,
                version,
            )
            count += 1
        if tag:
            add_string_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_TAG,
                tag,
                version,
            )
            count += 1
        if val1 is not None:
            add_int_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_VAL1,
                val1,
                version,
            )
            count += 1
        if val2 is not None:
            add_int_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_VAL2,
                val2,
                version,
            )
            count += 1
        if val3 is not None:
            add_int_change(
                db_changes,
                constants.TABLE_CLUB,
                uid,
                constants.PROP_CLUB_VAL3,
                val3,
                version,
            )
            count += 1

    LOGGER.info("Applied %s club changes from %s", count, csv_path)
    return count


def apply_nation_changes_from_csv(db_changes: ET.Element, version: int, csv_path: str) -> int:
    """Apply nation changes from *csv_path* and return the number of edits."""

    count = 0
    for line_no, row in _load_rows(csv_path):
        uid = parse_int(row.get("nation_uid"))
        if uid is None:
            LOGGER.error("Invalid or missing nation_uid on line %s in %s", line_no, csv_path)
            continue

        name = normalise_optional(row.get("name"))
        short_name = normalise_optional(row.get("short_name"))
        three_letter = normalise_optional(row.get("three_letter"))
        adjective = normalise_optional(row.get("adjective"))

        if name:
            add_string_change(
                db_changes,
                constants.TABLE_NATION,
                uid,
                constants.PROP_NATION_NAME,
                name,
                version,
            )
            count += 1
        if short_name:
            add_string_change(
                db_changes,
                constants.TABLE_NATION,
                uid,
                constants.PROP_NATION_SHORT,
                short_name,
                version,
            )
            count += 1
        if three_letter:
            add_string_change(
                db_changes,
                constants.TABLE_NATION,
                uid,
                constants.PROP_NATION_CODE3,
                three_letter,
                version,
            )
            count += 1
        if adjective:
            add_string_change(
                db_changes,
                constants.TABLE_NATION,
                uid,
                constants.PROP_NATION_ADJ,
                adjective,
                version,
            )
            count += 1

    LOGGER.info("Applied %s nation changes from %s", count, csv_path)
    return count


def apply_continent_changes_from_csv(db_changes: ET.Element, version: int, csv_path: str) -> int:
    """Apply continent changes from *csv_path* and return the number of edits."""

    count = 0
    for line_no, row in _load_rows(csv_path):
        uid = parse_int(row.get("continent_uid"))
        if uid is None:
            LOGGER.error("Invalid or missing continent_uid on line %s in %s", line_no, csv_path)
            continue

        name = normalise_optional(row.get("name"))
        if name:
            add_string_change(
                db_changes,
                constants.TABLE_CONTINENT,
                uid,
                constants.PROP_CONT_NAME,
                name,
                version,
            )
            count += 1

    LOGGER.info("Applied %s continent changes from %s", count, csv_path)
    return count


__all__ = [
    "apply_competition_changes_from_csv",
    "apply_club_changes_from_csv",
    "apply_nation_changes_from_csv",
    "apply_continent_changes_from_csv",
]
