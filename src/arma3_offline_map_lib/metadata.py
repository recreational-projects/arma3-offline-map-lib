"""Module containing `metadata` class."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Self

from attrs import define, field, validators

from .position_2d import Position2D

if TYPE_CHECKING:
    from pathlib import Path


@define(kw_only=True, frozen=True)
class Metadata:
    """Partial support for [grad_meh](https://github.com/gruppe-adler/grad_meh)
    'meta.json'.
    """

    world_name: str = field(validator=validators.instance_of(str))
    """ID of map
    (corresponds to LOWERCASE configName MAP_CONFIG)."""
    author: str = field(validator=validators.instance_of(str))
    """Map author
    (corresponds to MAP_CONFIG >> "author")."""
    display_name: str = field(validator=validators.instance_of(str))
    """Display name
    (corresponds to MAP_CONFIG >> "description")."""
    world_size: int = field(validator=validators.instance_of(int))
    """Size of map in meters
    (corresponds to MAP_CONFIG >> "mapSize".)"""
    grid_offset: Position2D
    """Offset (in m) of grid origin
    (corresponds to MAP_CONFIG >> "Grid" >> "offsetX" / "offsetY")."""
    elevation_offset: float = field(validator=validators.instance_of(float))
    """Offset (in m) of DEM values from 0 ASL
    (corresponds to MAP_CONFIG >> "elevationOffset")."""
    version: str = field(validator=validators.instance_of(str))
    """Version of `grad_meh`
    (This follows semantic versioning)."""

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """Return an instance from a 'meta.json' file.

        File must exist.
        """
        with path.open("rt") as fp:
            data_ = json.load(fp)

        return cls(
            world_name=data_["worldName"],
            author=data_["author"],
            display_name=data_["displayName"],
            world_size=data_["worldSize"],
            grid_offset=Position2D(data_["gridOffsetX"], data_["gridOffsetY"]),
            elevation_offset=data_["elevationOffset"],
            version=data_["version"],
        )
