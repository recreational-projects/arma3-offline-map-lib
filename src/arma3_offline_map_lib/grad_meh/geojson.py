"""Provides an interface for Arma 3 object location GeoJSON data
exported by [`gruppe-adler/grad_meh`](https://github.com/gruppe-adler/grad_meh).

Ref: https://github.com/gruppe-adler/grad_meh/blob/master/docs/geojson_spec.md

Classes derived from https://msgspec.dev/examples/geojson.
"""

from __future__ import annotations

import gzip
import logging
from typing import TYPE_CHECKING

import msgspec

if TYPE_CHECKING:
    from pathlib import Path

    from arma3_offline_map_lib.types_ import DictNode

type Position = tuple[float, float]

_LOGGER = logging.getLogger(__name__)


def geojson_gz_files_in_dir(path: Path) -> list[Path]:
    """Return all `*.geojson.gz` files in `path`."""
    return [p for p in list(path.iterdir()) if p.suffixes == [".geojson", ".gz"]]


def load_features_from_file(path: Path) -> list[Feature]:
    """Load GeoJSON features from a file (`*.geojson.gz`),
    as exported by `gruppe-adler/grad_meh`.

    NB: These files are gzipped arrays of GeoJSON features,
    not GeoJSON compliant files.
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

    properties: DictNode
    geometry: Geometry
    _id: str | int | None = None


class Point(msgspec.Struct, tag=True):
    """Point `Geometry` type."""

    coordinates: Position


class LineString(msgspec.Struct, tag=True):
    """LineString `Geometry` type."""

    coordinates: list[Position]


class Polygon(msgspec.Struct, tag=True):
    """Polygon `Geometry` type."""

    coordinates: list[list[Position]]


class MultiPolygon(msgspec.Struct, tag=True):
    """MultiPolygon `Geometry` type."""

    coordinates: list[list[list[Position]]]


Geometry = Point | LineString | Polygon | MultiPolygon
# Full GeoJSON implementation needs MultiPoint, MultiLineString, GeometryCollection
