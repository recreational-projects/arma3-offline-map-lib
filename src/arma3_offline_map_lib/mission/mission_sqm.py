"""Parse a mission's `mission.sqm` file with `armaclass`."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Self

import armaclass
from attrs import define

from arma3_offline_map_lib.position_2d import Position2D

if TYPE_CHECKING:
    from pathlib import Path

    from arma3_offline_map_lib.types_ import DictNode

_LOGGER = logging.getLogger(__name__)


@define(kw_only=True, frozen=True)
class MissionSqm:
    """Data from a mission's `mission.sqm` file."""

    markers: list[Marker]
    """Markers from the file, excluding any with missing `name` or `position` value."""

    @classmethod
    def from_file(cls, filepath: Path) -> Self | None:
        """Parse a `mission.sqm` file."""
        with filepath.open(errors="ignore") as f:
            data = f.read()

        try:
            mission = armaclass.parse(data)
            log_msg = f"Parsed `{filepath}`."
            _LOGGER.debug(log_msg)
        except armaclass.ParseError:
            log_msg = f"Couldn't parse `{filepath}`; may be binarized."
            _LOGGER.warning(log_msg)
            return None

        markers_ = _collect_markers(mission["Mission"])
        return cls(markers=markers_)


@define(kw_only=True, frozen=True)
class Marker:
    """Represents a map marker."""

    name: str
    position: Position2D

    @classmethod
    def from_mission_sqm_data(cls, data: DictNode) -> Self:
        """Construct `Marker` from data parsed from `mission.sqm`."""
        name_ = data.get("name")
        position_ = data.get("position")
        if name_ is None:
            err_msg = "Marker name is missing"
            raise ValueError(err_msg)

        if position_ is None:
            err_msg = "Marker position is missing"
            raise ValueError(err_msg)

        return cls(
            name=data["name"],
            position=Position2D.from_a3_position(position_),
        )


def _collect_markers(node: DictNode) -> list[Marker]:
    """Return `node`'s relevant descendants as `Marker`s, recursively.

    NB: ignores markers with missing `name` or `position` value.
    """
    markers = []
    for e in _get_entities(node):
        try:
            marker = Marker.from_mission_sqm_data(e)
            markers.append(marker)
        except ValueError:
            continue

    for layer_node in _get_child_layers(node):
        markers.extend(_collect_markers(layer_node))

    return markers


def _get_child_layers(node: DictNode) -> list[DictNode]:
    """Return `node`'s child layers."""
    return [e for e in _get_entities(node) if e.get("dataType") == "Layer"]


def _get_entities(node: DictNode) -> list[DictNode]:
    """Return `node`'s relevant data dict children."""
    if "Entities" not in node:
        return []

    return [e for e in node["Entities"].values() if isinstance(e, dict)]
