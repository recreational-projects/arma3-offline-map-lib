"""Partial implementation of GeoJSON spec.

Derived from https://jcristharif.com/msgspec/examples/geojson.html.
"""

from __future__ import annotations

import gzip
import logging
from typing import TYPE_CHECKING, Any

import msgspec

if TYPE_CHECKING:
    from pathlib import Path

LOGGER = logging.getLogger(__name__)

type _DictNode = dict[str, Any]
type _Position = tuple[float, float]


def geojson_gz_files_in_dir(path: Path) -> list[Path]:
    """Return all `*.geojson.gz` files in `path`."""
    return [p for p in list(path.iterdir()) if p.suffixes == [".geojson", ".gz"]]


def load_features_from_file(path: Path) -> list[Feature]:
    """Load GeoJSON features from a `.geojson.gz` file.

    NB: grad_meh source files are gzipped JSON arrays of GeoJSON features, not GeoJSON
    compliant files.
    """
    with gzip.open(path, "rt", encoding="utf-8") as file:
        try:
            features = msgspec.json.decode(file.read(), type=list[Feature])
        except msgspec.ValidationError as err:
            err_msg = f"Error decoding JSON: {path}."
            raise ValueError(err_msg) from err

    return features


class Feature(msgspec.Struct, tag=True):
    """Feature class."""

    geometry: Point
    properties: _DictNode
    id: str | int | None = None


class Point(msgspec.Struct, tag=True):
    """Point Geometry type."""

    coordinates: _Position
