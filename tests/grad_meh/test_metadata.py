"""Tests for `Metadata` class."""

from pathlib import Path

from arma3_offline_map_lib.grad_meh.metadata import Metadata


def test_from_file_happy_path() -> None:
    """Tests that `Metadata.from_file()` returns a valid `Metadata` object."""
    # arrange
    path = Path(__file__).parent / "test_meta.json"
    # act
    m = Metadata.from_file(path)
    # assert
    assert m
    assert m.world_name == "the_terrain"
    assert m.author == "The Author"
    assert m.display_name == "The Terrain"
    assert m.world_size == 8192
    assert m.grid_offset.x == 0
    assert m.grid_offset.y == 8192
    assert m.elevation_offset == 0.0
    assert m.version == "1.0.0-beta.4"
