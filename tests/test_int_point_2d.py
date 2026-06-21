"""Tests for `IntPoint2D` class."""

import pytest

from arma3_offline_map_lib.int_point_2d import IntPoint2D


def test_create_from_int() -> None:
    """Test creating IntPoint2D from int."""
    # arrange
    # act
    p = IntPoint2D(1, 2)
    # assert
    assert p


def test_create_from_float() -> None:
    """Test creating Point2D from float."""
    # arrange
    # act, assert
    with pytest.raises(TypeError):
        _p = IntPoint2D(-0.3, 4.776765)
