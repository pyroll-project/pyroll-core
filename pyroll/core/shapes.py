from typing import Iterable

import numpy as np
import shapely.geometry
from shapely.ops import linemerge
import logging

from pyroll.core.repr import ReprMixin
from shapely.geometry import MultiLineString, Point


# noinspection PyAbstractClass
class Polygon(shapely.geometry.Polygon, ReprMixin):
    @property
    def height(self) -> float:
        """Computes the height of the bounding box."""
        return self.bounds[3] - self.bounds[1]

    @property
    def width(self) -> float:
        """Computes the width of the bounding box."""
        return self.bounds[2] - self.bounds[0]

    @property
    def perimeter(self) -> float:
        """Get the perimeter of the Polygon (alias of ``Polygon.length``)."""
        return self.length

    @property
    def __attrs__(self):
        return {
            "width": self.width,
            "height": self.height,
            "perimeter": self.perimeter,
            "area": self.area,
        }

    __str__ = ReprMixin.__str__


_RECTANGLE_CORNERS = np.asarray([
    (-0.5, -0.5),
    (0.5, -0.5),
    (0.5, 0.5),
    (-0.5, 0.5)
])


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


shapely.geometry.Polygon = Polygon


class LineString(shapely.geometry.LineString, ReprMixin):
    @property
    def depth(self) -> float:
        """Computes the height of the bounding box."""
        return self.bounds[3] - self.bounds[1]

    @property
    def width(self) -> float:
        """Computes the width of the bounding box."""
        return self.bounds[2] - self.bounds[0]

    @property
    def __attrs__(self):
        return {
            "width": self.width,
            "depth": self.depth,
            "length": self.length,
        }

    __str__ = ReprMixin.__str__


shapely.geometry.LineString = LineString


def linemerge_if_multi(lines):
    if isinstance(lines, MultiLineString) or isinstance(lines, Iterable):
        merged_line = linemerge(lines)

        if isinstance(merged_line, MultiLineString):

            logging.getLogger(__name__).warning(
                "Discontinuous LineStrings for profile separation. Doing point wise comparison to resolve."
            )

            line_lengths = [line.length for line in merged_line.geoms]
            index_of_continuous_line = np.argmax(line_lengths)
            continuous_linestring = merged_line[index_of_continuous_line]

            discontinuous_lines = list(lines)
            discontinuous_lines.pop(index_of_continuous_line)

            points_representation_of_discontinuous_lines = [Point(p) for l in discontinuous_lines for p in l.coords]

            distances_of_points_to_continuous_line = [continuous_linestring.distance(p) for p in
                                                      points_representation_of_discontinuous_lines]

            if max(distances_of_points_to_continuous_line) <= line_lengths[index_of_continuous_line] / 1000:
                return continuous_linestring

            else:
                logging.getLogger(__name__).error(
                    f"Could not resolve discontinuous LineStrings for profile separation."
                )
                raise RuntimeError("Could not resolve discontinuous LineStrings for profile separation.")

        return merged_line

    return lines
