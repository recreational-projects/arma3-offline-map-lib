"""Module containing IntPoint2D class."""

from attrs import define, field, validators


@define(frozen=True)
class IntPoint2D:
    """Simple 2D integer point."""

    x: int = field(validator=validators.instance_of(int))
    y: int = field(validator=validators.instance_of(int))
