"""Parse a mission's `mission.sqm` file with `armaclass`."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Literal, Self

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
    """Markers from all layers."""

    @classmethod
    def from_file(cls, filepath: Path) -> Self:
        """Parse a `mission.sqm` file. Must not be binarized."""
        with filepath.open(errors="ignore") as f:
            data = f.read()

        mission_sqm_data = armaclass.parse(data)
        markers_ = _collect_markers(mission_sqm_data["Mission"])
        return cls(markers=markers_)


@define(kw_only=True, frozen=True)
class Marker:
    """Represents a map marker."""

    name: str
    """Corresponds to 'Variable Name' in the editor."""
    position: Position2D
    """NB: markers don't have a settable Z (height) position in the editor."""
    marker_type: Literal["ELLIPSE", "RECTANGLE"] | None
    """Area markers have a value; icon markers have `None`."""
    type_: str
    """For area markers, same as `marker_type`, but lowercase."""

    @classmethod
    def from_data(cls, data: DictNode) -> Self:
        """Construct `Marker` from data parsed from `mission.sqm`."""
        if data["dataType"] != "Marker":
            err_msg = "Can't construct Marker from non-marker data."
            raise ValueError(err_msg)

        return cls(
            name=data["name"],
            position=Position2D.from_a3_position(data["position"]),
            marker_type=data.get("markerType"),
            type_=data["type"],
        )


def _collect_markers(node: DictNode) -> list[Marker]:
    """Return `Marker` descendents of `node`, recursively."""
    markers = [
        Marker.from_data(e) for e in _get_entities(node) if e["dataType"] == "Marker"
    ]
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
