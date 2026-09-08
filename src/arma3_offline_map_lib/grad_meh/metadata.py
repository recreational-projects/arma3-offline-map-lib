"""Provides an interface for Arma 3 map metadata
exported by [`gruppe-adler/grad_meh`](https://github.com/gruppe-adler/grad_meh).

Ref: https://github.com/gruppe-adler/grad_meh/blob/master/docs/metajson_spec.md
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Self

from attrs import define, field
from attrs.validators import instance_of

from arma3_offline_map_lib.position_2d import Position2D

if TYPE_CHECKING:
    from pathlib import Path


@define(kw_only=True, frozen=True)
class Metadata:
    """Partial support for [grad_meh](https://github.com/gruppe-adler/grad_meh)
    'meta.json'.
    """

    world_name: str = field(validator=instance_of(str))
    """ID of map."""
    author: str = field(validator=instance_of(str))
    """Map author."""
    display_name: str = field(validator=instance_of(str))
    """Display name."""
    world_size: int = field(validator=instance_of(int))
    """Size of map in meters."""
    grid_offset: Position2D
    """Offset (in m) of grid origin."""
    elevation_offset: float = field(validator=instance_of(float))
    """Offset (in m) of DEM values from 0 ASL."""
    version: str = field(validator=instance_of(str))
    """Version of `grad_meh`."""

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """Return an instance from a 'meta.json' file,
        as exported by `gruppe-adler/grad_meh`.

        File must exist.
        """
        with path.open("rt") as fp:
            data_ = json.load(fp)

        return cls(
            world_name=data_["worldName"],
            author=data_["author"],
            display_name=data_["displayName"],
            world_size=data_["worldSize"],
            grid_offset=Position2D(x=data_["gridOffsetX"], y=data_["gridOffsetY"]),
            elevation_offset=data_["elevationOffset"],
            version=data_["version"],
        )
