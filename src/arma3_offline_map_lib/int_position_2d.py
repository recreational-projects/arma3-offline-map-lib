"""Module containing IntPosition2D class."""

from attrs import define, field, validators


@define(kw_only=True, frozen=True)
class IntPosition2D:
    """Simple 2D integer position.

    Hashable; keyword-only args.
    """

    x: int = field(validator=validators.instance_of(int))
    y: int = field(validator=validators.instance_of(int))
