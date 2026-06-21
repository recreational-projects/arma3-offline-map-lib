"""Module containing Point2D class."""

from attrs import define, field, validators


@define(frozen=True)
class Point2D:
    """Simple 2D point class.

    Hashable, unlike geojson library.
    Provides x and y keyword construction and properties,
    unlike geojson or pygeojson library.
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
