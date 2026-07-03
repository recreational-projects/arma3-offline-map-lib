"""Tests for `IntPosition2D` class."""

import pytest

from arma3_offline_map_lib.int_position_2d import IntPosition2D


def test_create_from_int() -> None:
    """Test creating from int."""
    # arrange
    # act
    p = IntPosition2D(x=1, y=2)
    # assert
    assert p


def test_create_from_float() -> None:
    """Test creating from float."""
    # arrange
    # act, assert
    with pytest.raises(TypeError):
        # pyrefly: ignore [bad-argument-type]
        _p = IntPosition2D(x=-0.3, y=4.776765)
