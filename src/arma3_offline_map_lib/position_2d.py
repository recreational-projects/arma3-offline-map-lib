"""Module containing Position2D class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from attrs import define, field, validators

if TYPE_CHECKING:
    from collections.abc import Sequence

    from . import geojson


@define(frozen=True)
class Position2D:
    """Simple 2D position class.

    Hashable; provides x and y keyword construction and properties.
    """

    x: int | float = field(
        validator=validators.or_(
            validators.instance_of(int), validators.instance_of(float)
        )
    )
    y: int | float = field(
        validator=validators.or_(
            validators.instance_of(int), validators.instance_of(float)
        )
    )

    @classmethod
    def from_a3_position(cls, seq: Sequence[float]) -> Self:
        """Construct `Position2D` from Arma 3 position, which has xy and xzy forms.

        Use when e.g. parsing `mission.sqm`.
        """
        return cls(x=seq[0], y=seq[-1])

    @classmethod
    def from_geojson_position(cls, position: geojson.Position) -> Self:
        """Construct `Position2D` from GeoJSON `Point`."""
        return cls(x=position[0], y=position[1])
