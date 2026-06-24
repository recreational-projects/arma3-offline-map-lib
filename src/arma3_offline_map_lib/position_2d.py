"""Module containing Position2D class."""

from attrs import define, field, validators


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
