"""Module containing DEM class."""

from __future__ import annotations

import gzip
from typing import TYPE_CHECKING, Self

import numpy as np
from attrs import define

from .int_position_2d import IntPosition2D
from .position_2d import Position2D

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray

_ESRI_ASCII_HEADER_PARAMETERS = {
    # ref https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/esri-ascii-raster-format.htm
    "NCOLS": "Number of cell columns",  # Integer greater than 0.
    "NROWS": "Number of cell rows",  # Integer greater than 0.
    "XLLCORNER": "X-coordinate of the origin (by lower left corner of the cell)",
    "YLLCORNER": "Y-coordinate of the origin (by lower left corner of the cell)",
    "CELLSIZE": "Cell size",  # Greater than 0.
    "NODATA_VALUE": "The input values to be NoData in the output raster",
    # Optional in spec. Default is -9999.
}


@define(kw_only=True, frozen=True)
class DEM:
    """Digital Elevation Model class, storing elevation as a NumPy array.

    Sufficient for [grad_meh](https://github.com/gruppe-adler/grad_meh) data.
    """

    elevation: NDArray[np.float16]
    cell_size: float

    @property
    def data_size(self) -> IntPosition2D:
        """Return data dimensions.

        Equivalent to ESRI ASCII `ncols, nrows`.
        """
        return IntPosition2D(self.elevation.shape[0], self.elevation.shape[1])

    @property
    def extents(self) -> Position2D:
        """Return physical dimensions in meters."""
        return Position2D(
            self.cell_size * self.data_size.x,
            self.cell_size * self.data_size.y,
        )

    @property
    def land(self) -> NDArray[np.bool]:
        """Return boolean array, where `True` indicates terrain above sea level."""
        return (self.elevation > 0).astype(bool)

    @property
    def land_area(self) -> float:
        """Return terrain above sea level in square meters."""
        return int(np.sum(self.land)) * self.cell_size**2

    @classmethod
    def from_esri_ascii_raster_gz(cls, file_path: Path) -> Self:
        """Load an ESRI ASCII raster from a gzipped file."""
        header = {}
        with gzip.open(file_path, "rt") as file:
            # `np.loadtxt(file)` does handle gzipped files, but we need the headers
            header_lines = [
                next(file) for _ in range(len(_ESRI_ASCII_HEADER_PARAMETERS))
            ]
            for line in header_lines:
                elements = line.split(" ", 1)
                if elements[0].upper() in _ESRI_ASCII_HEADER_PARAMETERS:
                    header[elements[0].upper()] = float(elements[1])

            data_array = np.loadtxt(file, dtype="float16")

        return cls(
            elevation=data_array,
            cell_size=header["CELLSIZE"],
        )
