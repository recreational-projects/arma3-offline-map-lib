"""Module containing Point2D class."""

from attrs import define, field, validators


@define(frozen=True)
class Point2D:
    """Simple 2D point class.

    Hashable, unlike geojson library.
    Provides x and y keyword construction and properties,
    unlike geojson or pygeojson library.
    """

    x: float = field(validator=validators.instance_of(float))
    y: float = field(validator=validators.instance_of(float))
