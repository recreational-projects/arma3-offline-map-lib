"""Tests for `Point2D` class."""

from arma3_offline_map_lib.point_2d import Point2D


def test_create_from_float_and_int() -> None:
    """Test creating Point2D from float and int."""
    # arrange
    # act
    p0 = Point2D(1, 2)
    p1 = Point2D(-0.3, 4.776765)
    p2 = Point2D(5.567, 2)
    # assert
    assert p0
    assert p1
    assert p2
