"""XML parsing and writing helpers for Football Manager editor files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple
from xml.etree import ElementTree as ET

LOGGER = logging.getLogger(__name__)


class EditorDataError(RuntimeError):
    """Raised when the base editor XML file does not match expectations."""


def load_editor_xml(path: str | Path) -> ET.ElementTree:
    """Load the Football Manager editor XML file located at *path*."""

    xml_path = Path(path)
    if not xml_path.exists():
        raise FileNotFoundError(f"Base XML file not found: {xml_path}")
    LOGGER.debug("Loading XML file %s", xml_path)
    return ET.parse(xml_path)


def get_root_and_version(tree: ET.ElementTree) -> Tuple[ET.Element, int]:
    """Return the root ``<record>`` element and database version integer."""

    root = tree.getroot()
    if root.tag != "record":
        raise EditorDataError("Root element is not <record> as expected")

    for child in root.findall("integer"):
        if child.get("id") == "version":
            value = child.get("value")
            if value is None:
                break
            try:
                version = int(value)
            except ValueError as exc:  # pragma: no cover - defensive programming
                raise EditorDataError("Version value is not an integer") from exc
            LOGGER.debug("Detected database version: %s", version)
            return root, version

    raise EditorDataError("Base XML does not include an <integer id=\"version\"> element")


def get_db_changes_list(root: ET.Element) -> ET.Element:
    """Return the ``<list id="db_changes">`` element, creating it if missing."""

    for child in root.findall("list"):
        if child.get("id") == "db_changes":
            LOGGER.debug("Found existing db_changes list with %s children", len(child))
            return child

    LOGGER.info("db_changes list missing; creating new list element")
    db_changes = ET.SubElement(root, "list", {"id": "db_changes"})
    return db_changes


def write_editor_xml(tree: ET.ElementTree, path: str | Path) -> None:
    """Write *tree* to *path* using UTF-16 encoding and an XML declaration."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.debug("Writing updated XML to %s", output_path)
    tree.write(output_path, encoding="utf-16", xml_declaration=True)


__all__ = [
    "EditorDataError",
    "load_editor_xml",
    "get_root_and_version",
    "get_db_changes_list",
    "write_editor_xml",
]
