"""Helpers for constructing Football Manager editor change records."""

from __future__ import annotations

import logging
from typing import Optional
from xml.etree import ElementTree as ET

from .utils import make_db_random_id

LOGGER = logging.getLogger(__name__)


def _base_change_record(
    db_changes: ET.Element,
    table_type: int,
    uid: int,
    property_id: int,
    version: int,
) -> ET.Element:
    """Create a new change ``<record>`` element with shared fields populated."""

    record = ET.SubElement(db_changes, "record")
    ET.SubElement(record, "integer", {"id": "database_table_type", "value": str(table_type)})
    ET.SubElement(record, "large", {"id": "db_unique_id", "value": str(uid)})
    ET.SubElement(record, "unsigned", {"id": "property", "value": str(property_id)})
    ET.SubElement(record, "integer", {"id": "version", "value": str(version)})
    LOGGER.debug(
        "Created base change record table=%s uid=%s property=%s version=%s",
        table_type,
        uid,
        property_id,
        version,
    )
    return record


def _attach_random_id(record: ET.Element, uid: int, property_id: int, new_value: str | int) -> None:
    """Attach a ``db_random_id`` element to *record* using a stable hash."""

    random_id = make_db_random_id(uid=uid, property_id=property_id, new_value=new_value)
    ET.SubElement(record, "integer", {"id": "db_random_id", "value": str(random_id)})
    LOGGER.debug("Attached db_random_id=%s", random_id)


def add_string_change(
    db_changes: ET.Element,
    table_type: int,
    uid: int,
    property_id: int,
    new_value: str,
    version: int,
    old_value: Optional[str] = None,
) -> ET.Element:
    """Append a string change record to *db_changes* and return it."""

    record = _base_change_record(db_changes, table_type, uid, property_id, version)
    ET.SubElement(record, "string", {"id": "new_value", "value": new_value})
    if old_value is not None:
        ET.SubElement(record, "string", {"id": "odvl", "value": old_value})
    ET.SubElement(record, "boolean", {"id": "is_client_field", "value": "true"})
    ET.SubElement(record, "boolean", {"id": "is_language_field", "value": "true"})
    _attach_random_id(record, uid, property_id, new_value)
    LOGGER.info(
        "Queued string change table=%s uid=%s property=%s value=%s",
        table_type,
        uid,
        property_id,
        new_value,
    )
    return record


def add_int_change(
    db_changes: ET.Element,
    table_type: int,
    uid: int,
    property_id: int,
    new_value: int,
    version: int,
    old_value: Optional[int] = None,
) -> ET.Element:
    """Append an integer change record to *db_changes* and return it."""

    record = _base_change_record(db_changes, table_type, uid, property_id, version)
    ET.SubElement(record, "integer", {"id": "new_value", "value": str(new_value)})
    if old_value is not None:
        ET.SubElement(record, "integer", {"id": "odvl", "value": str(old_value)})
    _attach_random_id(record, uid, property_id, new_value)
    LOGGER.info(
        "Queued integer change table=%s uid=%s property=%s value=%s",
        table_type,
        uid,
        property_id,
        new_value,
    )
    return record


__all__ = [
    "add_string_change",
    "add_int_change",
]
