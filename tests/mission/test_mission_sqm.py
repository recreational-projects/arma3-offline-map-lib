"""Tests for `MissionSqm` class."""

from pathlib import Path

from arma3_offline_map_lib.mission.mission_sqm import MissionSqm


def test_mission_sqm_from_file_happy_path() -> None:
    """Tests that `MissionSqm.from_file()` returns a valid `MissionSqm` object."""
    # arrange
    path = Path(__file__).parent / "au_stratis_mission.sqm"
    # act
    mission_sqm = MissionSqm.from_file(path)
    # assert
    assert mission_sqm
    assert len(mission_sqm.markers) == 75


def test_area_marker_happy_path() -> None:
    """Tests area `Marker`."""
    # arrange
    path = Path(__file__).parent / "au_stratis_mission.sqm"
    mission_sqm = MissionSqm.from_file(path)
    # act
    marker = mission_sqm.markers[0]
    # assert
    assert marker.position.x == 1784.4497
    assert marker.position.y == 5770.7554
    # assert marker.position.z == 172.01591  # noqa: ERA001
    assert marker.name == "airp_1_mortar"
    assert marker.marker_type == "ELLIPSE"
    assert marker.type_ == "ellipse"


def test_icon_marker_happy_path() -> None:
    """Tests icon `Marker`."""
    # arrange
    path = Path(__file__).parent / "au_stratis_mission.sqm"
    mission_sqm = MissionSqm.from_file(path)
    # act
    marker = mission_sqm.markers[16]
    # assert
    assert marker
    assert marker.position.x == 2058.5933
    assert marker.position.y == 5832.1191
    # assert marker.position.z == 183.92276  # noqa: ERA001
    assert marker.name == "spawnPoint_1"
    assert marker.marker_type is None
    assert marker.type_ == "hd_start"
