"""Module containing IntPosition2D class."""

from attrs import define, field, validators


@define(frozen=True)
class IntPosition2D:
    """Simple 2D integer position.

    Hashable; provides x and y keyword construction and properties.
    """

    x: int = field(validator=validators.instance_of(int))
    y: int = field(validator=validators.instance_of(int))
