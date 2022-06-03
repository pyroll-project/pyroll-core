import logging
import math
from typing import Optional

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import Point, LinearRing, Polygon, LineString
from shapely.ops import clip_by_rect

from pyroll.core.grooves import GrooveBase
from pyroll.core.plugin_host import PluginHost

_log = logging.getLogger(__name__)


class Profile(PluginHost):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        super().__init__(dict(
            profile=self
        ))

    @classmethod
    def from_groove(
            cls,
            groove: GrooveBase,
            width: Optional[float] = None,
            filling: Optional[float] = None,
            height: Optional[float] = None,
            gap: Optional[float] = None,
            **kwargs
    ) -> 'Profile':
        """
        Create a profile instance based on a given groove.
        The dimensioning of the profile is determined by the parameters ``width``, ``filling``, ``height`` and ``gap``.
        Give exactly one of ``width`` and ``filling``.
        Give exactly one of ``height`` and ``gap``.

        :param groove: the groove the profile should be created from
        :param width: the width of the resulting profile, must be > 0
        :param filling: the filling ratio of the groove, must be > 0
        :param height: the height of the profile, must be > 0
        :param gap: the gap between the groove contours (roll gap), must be >= 0
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises TypeError: on invalid argument combinations
        :raises ValueError: if arguments are out of range
        """

        if width is not None and filling is None:
            filling = width / groove.usable_width
        elif filling is not None and width is None:
            width = filling * groove.usable_width
        else:
            raise TypeError("either 'width' or 'filling' must be given")

        if height is not None and gap is None:
            gap = height - 2 * groove.depth
        elif gap is not None and height is None:
            height = gap + 2 * groove.depth
        else:
            raise TypeError("either 'gap' or 'height' must be given")

        if (
                filling <= 0
                or width <= 0
                or height <= 0
                or gap < 0

        ):
            raise ValueError("argument value(s) out of range")

        if filling > 1:
            _log.warning("Encountered overfilled groove in profile construction.")

        upper_contour_line = translate(groove.contour_line, yoff=gap / 2)
        lower_contour_line = translate(groove.contour_line, yoff=-gap / 2)

        return cls(
            upper_contour_line=upper_contour_line,
            lower_contour_line=lower_contour_line,
            height=height,
            width=width,
            types=groove.types,
            **kwargs
        )

    @classmethod
    def round(
            cls,
            radius: Optional[float] = None,
            diameter: Optional[float] = None,
            **kwargs
    ) -> 'Profile':
        """
        Creates a round shaped profile (a real circle round, without imperfections of round grooves).
        Give exactly one of ``radius`` and ``diameter``.

        :param radius: the radius of the round profile, must be > 0
        :param diameter: the diameter of the round profile, must be > 0
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises TypeError: on invalid argument combinations
        :raises ValueError: if arguments are out of range
        """

        if radius is not None and diameter is None:
            diameter = 2 * radius
        elif diameter is not None and radius is None:
            radius = diameter / 2
        else:
            raise TypeError("either 'radius' or 'diameter' must be given")

        if radius <= 0:
            raise ValueError("argument value(s) out of range")

        center = Point((0, 0))
        circle = center.buffer(radius)

        upper_contour_line = clip_by_rect(circle.boundary, -math.inf, 0, math.inf, math.inf)
        lower_contour_line = clip_by_rect(circle.boundary, -math.inf, -math.inf, math.inf, 0)

        return cls(
            upper_contour_line=upper_contour_line,
            lower_contour_line=lower_contour_line,
            height=diameter,
            width=diameter,
            types=["round"],
            **kwargs
        )

    @classmethod
    def square(
            cls,
            side: Optional[float] = None,
            diagonal: Optional[float] = None,
            corner_radius: float = 0,
            **kwargs
    ) -> 'Profile':
        """
        Creates a square shaped profile (a real square with rounded corners, without imperfections of square grooves).
        A square is oriented to stand on its corner, use :py:meth:`box` to create a side standing one.
        Give exactly one of ``side`` and ``diagonal``.

        :param side: the side length of the square profile, must be > 0
        :param diagonal: the diagonal's length of the square profile, must be > 0.
            Note, that the diagonal is measured at the tips, as if the corner radii were not present
            for consistency with :py:meth:`box`.
        :param corner_radius: the radius of the square's corners, must be >= 0 and <= side / 2
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises TypeError: on invalid argument combinations
        :raises ValueError: if arguments are out of range
        """

        if side is not None and diagonal is None:
            diagonal = np.sqrt(2) * side
        elif diagonal is not None and side is None:
            side = diagonal / np.sqrt(2)
        else:
            raise TypeError("either 'side' or 'diagonal' must be given")

        if (
                side <= 0
                or corner_radius < 0
                or corner_radius > side / 2
        ):
            raise ValueError("argument value(s) out of range")

        line = LinearRing(np.array([(1, 0), (0, 1), (-1, 0), (0, -1)]) * (diagonal / 2 - corner_radius * np.sqrt(2)))
        if corner_radius != 0:
            polygon = line.buffer(corner_radius)
        else:
            polygon = Polygon(line)

        upper_contour_line = clip_by_rect(polygon.exterior, -math.inf, 0, math.inf, math.inf)
        lower_contour_line = rotate(upper_contour_line, angle=180, origin=(0, 0))

        actual_diagonal = upper_contour_line.bounds[2] - upper_contour_line.bounds[0]

        return cls(
            upper_contour_line=upper_contour_line,
            lower_contour_line=lower_contour_line,
            height=actual_diagonal,
            width=actual_diagonal,
            types=["square", "diamond"],
            **kwargs
        )


    @classmethod
    def box(
            cls,
            height: float,
            width: float,
            corner_radius: float = 0,
            **kwargs
    ) -> 'Profile':
        """
        Creates a box shaped profile (a real rectangular shape with rounded corners,
        without imperfections of box grooves).
        A box is oriented to stand on its side, use :py:meth:`square` to create a corner standing square.

        :param height: the height of the box profile, must be > 0
        :param width: the width of the box profile, must be > 0
        :param corner_radius: the radius of the square's corners, must be >= 0, <= height / 2 and <= width / 2
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises ValueError: if arguments are out of range
        """

        if (
                height <= 0
                or width <= 0
                or corner_radius < 0
                or corner_radius > height / 2
                or corner_radius > width / 2
        ):
            raise ValueError("argument value(s) out of range")

        line = LinearRing(np.array([(1, -1), (1, 1), (-1, 1), (-1, -1)])
                          * (width / 2 - corner_radius, height / 2 - corner_radius))
        if corner_radius != 0:
            polygon = line.buffer(corner_radius)
        else:
            polygon = Polygon(line)

        upper_contour_line = clip_by_rect(polygon.exterior, -math.inf, 0, math.inf, math.inf)
        lower_contour_line = rotate(upper_contour_line, angle=180, origin=(0, 0))

        return cls(
            upper_contour_line=upper_contour_line,
            lower_contour_line=lower_contour_line,
            height=height,
            width=width,
            types=["box"],
            **kwargs
        )

    @classmethod
    def diamond(
            cls,
            height: float,
            width: float,
            corner_radius: float = 0,
            **kwargs
    ) -> 'Profile':
        """
        Creates a diamond shaped profile (a real diamond shape with rounded corners,
        without imperfections of diamond grooves).
        A diamond is oriented to stand on its corner.

        :param height: the height of the diamond profile, must be > 0
        :param width: the width of the diamond profile, must be > 0
        :param corner_radius: the radius of the diamonds's corners, must be >= 0, <= height / 2 and <= width / 2
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises ValueError: if arguments are out of range
        """

        if (
                height <= 0
                or width <= 0
                or corner_radius < 0
                or corner_radius > height / 2
                or corner_radius > width / 2
        ):
            raise ValueError("argument value(s) out of range")

        line = LinearRing(np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])
                          * (width / 2 - corner_radius, height / 2 - corner_radius))
        if corner_radius != 0:
            polygon = line.buffer(corner_radius)
        else:
            polygon = Polygon(line)

        upper_contour_line = clip_by_rect(polygon.exterior, -math.inf, 0, math.inf, math.inf)
        lower_contour_line = rotate(upper_contour_line, angle=180, origin=(0, 0))

        return cls(
            upper_contour_line=upper_contour_line,
            lower_contour_line=lower_contour_line,
            height=height,
            width=width,
            types=["diamond"],
            **kwargs
        )

    def local_height(self, z: float) -> float:
        coords = np.array([(1, -1), (1, 1)]) * (z, self.height)

        vline = LineString(
            coords
        )

        intersection = vline.intersection(self.cross_section)

        return intersection.length

    def local_width(self, y: float) -> float:
        coords = np.array([(-1, 1), (1, 1)]) * (self.width, y)

        hline = LineString(
            coords
        )

        intersection = hline.intersection(self.cross_section)

        return intersection.length
