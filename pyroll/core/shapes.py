from typing import Iterable

import numpy as np
from shapely.geometry import Polygon, LineString, MultiLineString, Point
from shapely.ops import linemerge
import logging

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


def height(self) -> float:
    return self.bounds[3] - self.bounds[1]


def width(self) -> float:
    return self.bounds[2] - self.bounds[0]


def perimeter(self) -> float:
    return self.length


Polygon.height = property(height)
"""Computes the height of the bounding box."""
Polygon.width = property(width)
"""Computes the width of the bounding box."""
Polygon.perimeter = property(perimeter)
"""Get the perimeter of the Polygon (alias of ``Polygon.length``)."""

LineString.height = property(height)
"""Computes the height of the bounding box."""
LineString.width = property(width)
"""Computes the width of the bounding box."""

polygon_repr_attrs = ["height", "width", "area", "length"]


def polygon_repr_pretty(self, p, cycle):
    if cycle:
        p.text(
            type(self).__qualname__ + "(...)"
        )
        return

    with p.group(4, "Polygon(", ")"):
        p.break_()
        for attr in polygon_repr_attrs:
            p.text(attr)
            p.text("=")
            p.pretty(getattr(self, attr))
            p.text(",")
            p.breakable()


Polygon._repr_pretty_ = polygon_repr_pretty

line_repr_attrs = ["depth", "width", "length"]


def line_repr_pretty(self, p, cycle):
    if cycle:
        p.text(
            type(self).__qualname__ + "(...)"
        )
        return

    with p.group(4, "LineString(", ")"):
        p.break_()
        for attr in line_repr_attrs:
            p.text(attr)
            p.text("=")
            p.pretty(getattr(self, attr))
            p.text(",")
            p.breakable()


LineString._repr_pretty_ = polygon_repr_pretty


def linemerge_if_multi(lines):
    if isinstance(lines, MultiLineString) or isinstance(lines, Iterable):
        merged_line = linemerge(lines)

        if isinstance(merged_line, MultiLineString) or isinstance(merged_line, Iterable):
            logging.getLogger(__name__).warning(
                "Discontinuous LineStrings for profile separation. Doing point wise comparison to resolve."
            )

            line_lengths = [line.length for line in lines.geoms]
            index_of_continuous_line = np.argmax(line_lengths)
            continuous_linestring = lines[index_of_continuous_line]

            discontinuous_lines = []
            for i in range(len(lines)):
                if i != index_of_continuous_line:
                    discontinuous_lines.append(np.asarray(lines[i]))

            points_representation_of_discontinuous_lines = []
            for discontinuous_line in discontinuous_lines:
                for point_coordinates in discontinuous_line:
                    points_representation_of_discontinuous_lines.append(Point(point_coordinates))

            distances_of_points_to_continuous_line = []
            for point in points_representation_of_discontinuous_lines:
                distances_of_points_to_continuous_line.append(continuous_linestring.distance(point))

            if max(distances_of_points_to_continuous_line) <= 10 ** -4:
                return continuous_linestring

            else:
                logging.getLogger(__name__).error(
                    f"Could not resolve discontinuous LineStrings for profile separation."
                )
                raise RuntimeError("Could not resolve discontinuous LineStrings for profile separation.")

        return merged_line

    return lines
