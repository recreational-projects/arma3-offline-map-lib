"""Provides a `Position2D` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from attrs import define, field
from attrs.validators import instance_of, or_

if TYPE_CHECKING:
    from collections.abc import Sequence

    from arma3_offline_map_lib.grad_meh import geojson


@define(kw_only=True, frozen=True)
class Position2D:
    """Simple 2D position class.

    Keyword-only args. Hashable.
    """

    x: float = field(validator=or_(instance_of(int), instance_of(float)))
    """Meter units."""
    y: float = field(validator=or_(instance_of(int), instance_of(float)))
    """Meter units."""

    @classmethod
    def from_a3_position(cls, seq: Sequence[float]) -> Self:
        """Construct `Position2D` from an Arma 3 internal position,
        which has `x, y` and `x, z, y` forms with meter units. `z` is ignored.

        Used e.g. when parsing `mission.sqm`.
        """
        return cls(x=seq[0], y=seq[-1])

    @classmethod
    def from_geojson_position(cls, position: geojson.Position) -> Self:
        """Construct `Position2D` from GeoJSON-like `Position`
        used by [`gruppe-adler/grad_meh`](https://github.com/gruppe-adler/grad_meh)
        and `arma3_offline_map_lib.grad_meh.geojson,` which uses `y, x` form.
        """
        return cls(x=position[0], y=position[1])
