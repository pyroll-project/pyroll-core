from typing import Iterable

import numpy as np
import shapely.geometry as geo
from shapely.ops import linemerge

_RECTANGLE_CORNERS = np.asarray([
    (-0.5, -0.5),
    (0.5, -0.5),
    (0.5, 0.5),
    (-0.5, 0.5)
])


# noinspection PyAbstractClass
class Polygon(geo.Polygon):
    """
    A subclass of shapely's Polygon with some additional computed properties for convenience.
    """

    @property
    def height(self) -> float:
        """Computes the height of the bounding box."""
        return self.bounds[3] - self.bounds[1]

    @property
    def width(self) -> float:
        """Computes the width of the bounding box."""
        return self.bounds[2] - self.bounds[0]

    _repr_attrs = ["height", "width", "area", "length"]

    def __repr__(self):
        return (
                "Polygon("
                + ", ".join(f"{attr}={getattr(self, attr)}" for attr in self._repr_attrs)
                + ")"
        )


def rectangle(width: float, height: float):
    """
    Creates an instance of :py:class:`Polygon` with rectangular shape from height and width aligned to the axes.

    :param width: the width of the rectangle
    :param height: the height of the rectangle
    """

    try:
        width = float(width)
        height = float(height)

    except TypeError as e:
        raise TypeError("width and height must be convertible to float") from e

    points = _RECTANGLE_CORNERS * (width, height)
    rect = Polygon(points)

    return rect


class ContourLine(geo.LineString):
    """
    A subclass of shapely's LineString representing a contour line with some additional computed properties for convenience.
    """

    @property
    def depth(self) -> float:
        """Computes the height of the bounding box."""
        return self.bounds[3] - self.bounds[1]

    @property
    def width(self) -> float:
        """Computes the width of the bounding box."""
        return self.bounds[2] - self.bounds[0]

    _repr_attrs = ["depth", "width", "length"]

    def __repr__(self):
        return (
                "ContourLine("
                + ", ".join(f"{attr}={getattr(self, attr)}" for attr in self._repr_attrs)
                + ")"
        )


def linemerge_if_multi(lines):
    if isinstance(lines, geo.MultiLineString) or isinstance(lines, Iterable):
        return linemerge(lines)
    return lines
