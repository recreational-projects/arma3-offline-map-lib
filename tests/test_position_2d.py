"""Tests for `Position2D` class."""

from arma3_offline_map_lib.position_2d import Position2D


def test_create_from_float_and_int() -> None:
    """Test creating from float and int."""
    # arrange
    # act
    p0 = Position2D(1, 2)
    p1 = Position2D(-0.3, 4.776765)
    p2 = Position2D(5.567, 2)
    # assert
    assert p0
    assert p1
    assert p2
