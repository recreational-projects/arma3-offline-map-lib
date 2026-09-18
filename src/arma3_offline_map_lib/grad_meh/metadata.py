"""Provides an interface for Arma 3 map metadata
exported by [`gruppe-adler/grad_meh`](https://github.com/gruppe-adler/grad_meh).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Self

from attrs import define, field
from attrs.validators import deep_iterable, instance_of, le, max_len, min_len

from arma3_offline_map_lib.position_2d import Position2D

if TYPE_CHECKING:
    from pathlib import Path


@define(kw_only=True, frozen=True)
class Metadata:
    """Support for metadata exported
    by [grad_meh](https://github.com/gruppe-adler/grad_meh).

    Ref: https://github.com/gruppe-adler/grad_meh/blob/master/docs/metajson_spec.md
    """

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """Return an instance from a `meta.json` file,
        as exported by `gruppe-adler/grad_meh`.

        File must exist.
        """
        with path.open("rt") as fp:
            data_ = json.load(fp)

        return cls(
            world_name=data_["worldName"],
            author=data_["author"],
            display_name=data_["displayName"],
            grid_offset=Position2D(x=data_["gridOffsetX"], y=data_["gridOffsetY"]),
            latitude=data_["latitude"],
            longitude=data_["longitude"],
            elevation_offset=data_["elevationOffset"],
            version=data_["version"],
            color_outside=tuple(data_["colorOutside"]),
            world_size=data_["worldSize"],
        )

    world_name: str = field(validator=instance_of(str))
    """ID of map."""
    author: str = field(validator=instance_of(str))
    """Map author."""
    display_name: str = field(validator=instance_of(str))
    """Map display name."""
    elevation_offset: float = field(validator=instance_of(float))
    """Offset in meters of DEM values from 0 ASL."""
    grid_offset: Position2D
    """Offset in meters of grid origin."""
    latitude: float = field(validator=instance_of(float))
    """Latitude of map."""
    longitude: float = field(validator=instance_of(float))
    """Longitude of map."""
    version: str = field(validator=instance_of(str))
    """Version of [`gruppe-adler/grad_meh`](https://github.com/gruppe-adler/grad_meh)
    that exported the metadata."""
    color_outside: tuple[float, float, float, float] | None = field(
        default=None,
        validator=deep_iterable(
            member_validator=(instance_of(float), le(1)),
            iterable_validator=(instance_of(tuple), min_len(4), max_len(4)),
        ),
    )
    """Outside color of map, in `r, g, b, a` form. Each value is a float <= 1.

    Optional."""
    world_size: int = field(validator=instance_of(int))
    """Size of map in meters. Arma 3 maps are square."""

    # unsupported attributes: grids
