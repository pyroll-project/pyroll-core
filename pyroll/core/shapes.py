import numpy as np

from pyroll.core.repr import ReprMixin
from shapely import Polygon, LineString


# noinspection PyAbstractClass
class PatchedPolygon(Polygon):
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


Polygon.height = PatchedPolygon.height
Polygon.width = PatchedPolygon.width
Polygon.perimeter = PatchedPolygon.perimeter
Polygon.__attrs__ = PatchedPolygon.__attrs__
Polygon.__str__ = ReprMixin.__str__
Polygon.__repr__ = ReprMixin.__repr__
# noinspection PyProtectedMember
Polygon._repr_html_ = ReprMixin._repr_html_
# noinspection PyProtectedMember
Polygon._repr_pretty_ = ReprMixin._repr_pretty_

_RECTANGLE_CORNERS = np.asarray(
    [
        (-0.5, -0.5),
        (0.5, -0.5),
        (0.5, 0.5),
        (-0.5, 0.5)
    ]
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


class PatchedLineString(LineString):
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


LineString.depth = PatchedLineString.depth
LineString.width = PatchedLineString.width
LineString.__attrs__ = PatchedLineString.__attrs__
LineString.__str__ = ReprMixin.__str__
LineString.__repr__ = ReprMixin.__repr__
# noinspection PyProtectedMember
LineString._repr_html_ = ReprMixin._repr_html_
# noinspection PyProtectedMember
LineString._repr_pretty_ = ReprMixin._repr_pretty_
