"""Module containing IntPoint2D class."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IntPoint2D:
    """2D integer point."""

    x: int
    y: int
