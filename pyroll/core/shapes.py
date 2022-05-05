from typing import Iterable

import numpy as np
from shapely.affinity import rotate
from shapely.geometry import Polygon, MultiLineString
from shapely.ops import linemerge

_RECTANGLE_CORNERS = np.asarray([
    (-0.5, -0.5),
    (0.5, -0.5),
    (0.5, 0.5),
    (-0.5, 0.5)
])


# noinspection PyAbstractClass
class Rectangle(Polygon):
    """
    A special rectangular Polygon built from width and height.
    Width and height are exposed as properties.

    Rectangle objects do not support transformations,
    since the constructor does not accept ``shell`` and ``hull`` arguments.
    The result may not be a rectangle anymore.
    Convert explicitly to a ``Polygon`` before using them (f.e. by using :py:meth:`to_polygon`).
    """

    def __init__(self, width: float, height: float):
        """
        :param width: the width of the rectangle
        :param height: the height of the rectangle
        """

        try:
            width = float(width)
            height = float(height)
            points = _RECTANGLE_CORNERS * (width, height)
            super().__init__(points)

            self.height = height
            """The height of the rectangle."""
            self.width = width
            """The width of the rectangle."""

        except TypeError as e:
            raise TypeError("width and height must be convertible to float") from e

    def to_polygon(self):
        return Polygon(self)


def linemerge_if_multi(lines):
    if isinstance(lines, MultiLineString) or isinstance(lines, Iterable):
        return linemerge(lines)
    return lines
