"""Provides an interface for Arma 3 digital elevation data
exported by [`gruppe-adler/grad_meh`](https://github.com/gruppe-adler/grad_meh).
"""

from __future__ import annotations

import gzip
from typing import TYPE_CHECKING, Self

import numpy as np
from attrs import define
from PIL import Image, ImageOps

from arma3_offline_map_lib.grad_meh.int_position_2d import IntPosition2D
from arma3_offline_map_lib.grad_meh.position_2d import Position2D

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray

_ESRI_ASCII_HEADER_PARAMETERS = {
    "NCOLS": "Number of cell columns",  # Integer greater than 0.
    "NROWS": "Number of cell rows",  # Integer greater than 0.
    "XLLCORNER": "X-coordinate of the origin (by lower left corner of the cell)",
    "YLLCORNER": "Y-coordinate of the origin (by lower left corner of the cell)",
    "CELLSIZE": "Cell size",  # Greater than 0.
    "NODATA_VALUE": "The input values to be NoData in the output raster",
    # Optional in spec. Default is -9999.
}

_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)


@define(kw_only=True, frozen=True)
class DEM:
    """Digital Elevation Model class, storing elevation as a NumPy array.

    Ref: https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/esri-ascii-raster-format.htm
    """

    elevation: NDArray[np.float16]
    """Elevation data."""
    cell_size: float
    """Equivalent to ESRI ASCII `CELLSIZE`."""

    @property
    def data_size(self) -> IntPosition2D:
        """Data dimensions.

        Equivalent to ESRI ASCII `NCOLS`, `NROWS`.
        """
        return IntPosition2D(x=self.elevation.shape[0], y=self.elevation.shape[1])

    @property
    def extents(self) -> Position2D:
        """Physical dimensions in meters."""
        return Position2D(
            x=self.cell_size * self.data_size.x,
            y=self.cell_size * self.data_size.y,
        )

    @property
    def land(self) -> NDArray[np.bool]:
        """Boolean array, where `True` indicates terrain above sea level."""
        return (self.elevation > 0).astype(bool)

    @property
    def land_area(self) -> float:
        """Area of terrain above sea level in square meters."""
        return int(np.sum(self.land)) * self.cell_size**2

    @classmethod
    def from_esri_ascii_raster_gz(cls, file_path: Path) -> Self:
        """Load an ESRI ASCII raster from a gzipped file (`*.asc.gz`),
        as exported by `gruppe-adler/grad_meh`.
        """
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

    def export_land_sea_image(
        self,
        *,
        path: Path,
        land_color: tuple[int, int, int],
        sea_color: tuple[int, int, int],
    ) -> None:
        """Export a image file,
        where land pixels are `land_color` and sea pixels are colored `sea_color`.
        """
        onebit_im = Image.fromarray(self.land)
        grayscale_im = onebit_im.convert(mode="L")
        color_im = ImageOps.colorize(grayscale_im, black=sea_color, white=land_color)
        color_im.save(path)
