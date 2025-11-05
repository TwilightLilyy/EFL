"""fm26_auto_editor command line interface.

This tool automates appending change records to Football Manager 2026
Pre-Game Editor XML files. Provide the base editor data export along with CSV
files describing the desired modifications. The tool converts each CSV row into
an XML ``<record>`` under ``<list id="db_changes">`` ready to re-import via the
Football Manager Pre-Game Editor.

Usage
-----
Run the tool via the module entry point::

    python -m fm26_auto_editor \
        --base-xml EorzeanFootball.xml \
        --out-xml EorzeanFootball_out.xml \
        --competitions-csv competitions.csv \
        --clubs-csv clubs.csv \
        --nations-csv nations.csv \
        --continents-csv continents.csv

Use ``--dry-run`` to preview how many changes would be generated without writing
an output file. CSV files must include the headers outlined in the project
requirements.
"""

from __future__ import annotations

import argparse
import logging
from typing import Dict, Iterable, Optional

from .importers import (
    apply_club_changes_from_csv,
    apply_competition_changes_from_csv,
    apply_continent_changes_from_csv,
    apply_nation_changes_from_csv,
)
from .utils import configure_logging
from .xml_model import (
    EditorDataError,
    get_db_changes_list,
    get_root_and_version,
    load_editor_xml,
    write_editor_xml,
)

LOGGER = logging.getLogger(__name__)


CATEGORY_APPLIERS = {
    "competitions": apply_competition_changes_from_csv,
    "clubs": apply_club_changes_from_csv,
    "nations": apply_nation_changes_from_csv,
    "continents": apply_continent_changes_from_csv,
}


def build_parser() -> argparse.ArgumentParser:
    """Construct the :class:`argparse.ArgumentParser` used by the CLI."""

    parser = argparse.ArgumentParser(
        prog="fm26_auto_editor",
        description="Append Football Manager 2026 editor change records from CSV files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--base-xml", required=True, help="Path to the base editor XML file")
    parser.add_argument(
        "--out-xml",
        required=True,
        help="Destination path for the updated editor XML file",
    )
    parser.add_argument("--competitions-csv", help="CSV describing competition changes")
    parser.add_argument("--clubs-csv", help="CSV describing club changes")
    parser.add_argument("--nations-csv", help="CSV describing nation changes")
    parser.add_argument("--continents-csv", help="CSV describing continent changes")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate change records but do not write the output file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity (can be specified multiple times)",
    )
    return parser


def _collect_csv_args(args: argparse.Namespace) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for category in CATEGORY_APPLIERS:
        attr = f"{category}_csv"
        value = getattr(args, attr)
        if value:
            mapping[category] = value
    return mapping


def _print_summary(changes_by_category: Dict[str, int]) -> None:
    lines = ["Change summary (dry-run):"]
    for category in CATEGORY_APPLIERS:
        count = changes_by_category.get(category, 0)
        lines.append(f"  {category}: {count}")
    print("\n".join(lines))


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Entry point for the ``fm26_auto_editor`` command line interface."""

    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    configure_logging(args.verbose)

    try:
        tree = load_editor_xml(args.base_xml)
    except FileNotFoundError as exc:
        LOGGER.error("%s", exc)
        return 1

    try:
        root, version = get_root_and_version(tree)
    except EditorDataError as exc:
        LOGGER.error("%s", exc)
        return 1

    db_changes = get_db_changes_list(root)
    csv_args = _collect_csv_args(args)

    if not csv_args:
        LOGGER.warning("No CSV files provided; nothing to do")

    changes_by_category: Dict[str, int] = {}
    for category, csv_path in csv_args.items():
        applier = CATEGORY_APPLIERS[category]
        LOGGER.info("Applying %s changes from %s", category, csv_path)
        changes_by_category[category] = applier(db_changes, version, csv_path)

    if args.dry_run:
        _print_summary(changes_by_category)
        return 0

    try:
        write_editor_xml(tree, args.out_xml)
    except OSError as exc:
        LOGGER.error("Failed to write output XML: %s", exc)
        return 1

    LOGGER.info("Wrote updated editor data to %s", args.out_xml)
    return 0


__all__ = ["build_parser", "main"]
