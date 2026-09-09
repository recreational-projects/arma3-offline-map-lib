"""Tests for `MissionSqm` class."""

from pathlib import Path

from arma3_offline_map_lib.mission.mission_sqm import MissionSqm


def test_mission_sqm_from_file_happy_path() -> None:
    """Tests that `MissionSqm.from_file()` returns a valid `MissionSqm` object."""
    # arrange
    path = Path(__file__).parent / "au_stratis_mission.sqm"
    # act
    m = MissionSqm.from_file(path)
    mission_sqm = MissionSqm.from_file(path)
    # assert
    assert m
    assert m.markers
    assert mission_sqm
    assert len(mission_sqm.markers) == 75
