import numpy as np

from pyroll.core.repr import ReprMixin
from shapely import Polygon, LineString, MultiPolygon, MultiLineString


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


for cls in [Polygon, MultiPolygon]:
    cls.height = PatchedPolygon.height
    cls.width = PatchedPolygon.width
    cls.perimeter = PatchedPolygon.perimeter
    cls.__attrs__ = PatchedPolygon.__attrs__
    cls.__str__ = ReprMixin.__str__
    cls.__repr__ = ReprMixin.__repr__
    # noinspection PyProtectedMember
    cls._repr_html_ = ReprMixin._repr_html_
    # noinspection PyProtectedMember
    cls._repr_pretty_ = ReprMixin._repr_pretty_

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
    def height(self) -> float:
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
            "height": self.height,
            "length": self.length,
        }


for cls in [LineString, MultiLineString]:
    cls.height = PatchedLineString.height
    cls.width = PatchedLineString.width
    cls.__attrs__ = PatchedLineString.__attrs__
    cls.__str__ = ReprMixin.__str__
    cls.__repr__ = ReprMixin.__repr__
    # noinspection PyProtectedMember
    cls._repr_html_ = ReprMixin._repr_html_
    # noinspection PyProtectedMember
    cls._repr_pretty_ = ReprMixin._repr_pretty_
