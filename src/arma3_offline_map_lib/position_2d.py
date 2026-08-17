"""Module containing Position2D class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from attrs import define, field, validators

if TYPE_CHECKING:
    from collections.abc import Sequence

    from . import geojson


@define(kw_only=True, frozen=True)
class Position2D:
    """Simple 2D position class.

    Hashable; keyword-only args.
    """

    x: float = field(
        validator=validators.or_(
            validators.instance_of(int), validators.instance_of(float)
        )
    )
    y: float = field(
        validator=validators.or_(
            validators.instance_of(int), validators.instance_of(float)
        )
    )

    @classmethod
    def from_a3_position(cls, seq: Sequence[float]) -> Self:
        """Construct `Position2D` from an Arma 3 internal position,
        which has (x, y) and (x, z, y) forms.

        Use when e.g. parsing `mission.sqm`.
        """
        return cls(x=seq[0], y=seq[-1])

    @classmethod
    def from_geojson_position(cls, position: geojson.Position) -> Self:
        """Construct `Position2D` from GeoJSON `Point` which has (lon, lat) form."""
        return cls(x=position[0], y=position[1])
