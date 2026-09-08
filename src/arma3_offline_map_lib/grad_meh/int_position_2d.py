"""Module containing IntPosition2D class."""

from attrs import define, field
from attrs.validators import instance_of


@define(kw_only=True, frozen=True)
class IntPosition2D:
    """Simple 2D integer position used internally. e.g. for grid dimensions.

    Hashable; keyword-only args.
    """

    x: int = field(validator=instance_of(int))
    y: int = field(validator=instance_of(int))
