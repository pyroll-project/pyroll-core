import logging
import math
from typing import Optional, Tuple, Iterable

import numpy as np
from shapely.affinity import translate
from shapely.geometry import Point, LinearRing, Polygon, LineString
from shapely.ops import clip_by_rect, unary_union

from ..grooves import GrooveBase
from ..hooks import HookHost, Hook

_log = logging.getLogger(__name__)


class Profile(HookHost):
    """Represents a profile aka a workpiece state."""

    cross_section = Hook[Polygon]()
    """Shape of the profile's cross-section."""

    types = Hook[Tuple[str, ...]]()
    """Classifiers of the profile's shape's type."""

    x = Hook[float]()
    """Spacial coordinate in rolling direction."""

    t = Hook[float]()
    """Temporal coordinate."""

    velocity = Hook[float]()
    """Mean material flow velocity."""

    height = Hook[float]()
    """Maximum height (y-direction)."""

    width = Hook[float]()
    """Maximum width (z-direction)."""

    length = Hook[float]()
    """Length of the workpiece (x-direction)."""

    equivalent_rectangle = Hook[Polygon]()
    """Equivalent rectangle geometry for use with equivalent flat pass models."""

    equivalent_height = Hook[float]()
    """Height of the equivalent rectangle."""

    equivalent_width = Hook[float]()
    """Width of the equivalent rectangle."""

    temperature = Hook[float]()
    """Mean temperature of the profile cross-section."""

    surface_temperature = Hook[float]()
    """Mean temperature of the profile surface."""

    core_temperature = Hook[float]()
    """Temperature of the profile core."""

    strain = Hook[float]()
    """Mean equivalent strain of the profile cross-section."""

    flow_stress = Hook[float]()
    """Mean flow stress of the profile material."""

    elastic_modulus = Hook[float]()
    """Mean elastic modulus of the profile material."""

    poissons_ratio = Hook[float]()
    """Mean Poisson's ratio of the profile material."""

    thermal_conductivity = Hook[float]()
    """Mean thermal conductivity of the profile material."""

    thermal_capacity = Hook[float]()
    """Mean thermal capacity of the profile material."""

    density = Hook[float]()
    """Mean density (specific weight) of the profile material."""

    material = Hook[str | Iterable[str]]()
    """String or sequence of strings classifying the material of the profile.
    Can be used by material databases to retrieve respective data."""

    def __init__(self, **kwargs):
        """Using the ``__init__`` is not recommended, use one of the factory class methods instead."""
        self.__dict__.update(kwargs)
        super().__init__()

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

        poly = Polygon(np.concatenate([
            upper_contour_line.coords,
            lower_contour_line.coords
        ]))

        if (
                # one percent tolerance to bypass discretization issues
                - width / 2 < poly.bounds[0] * 1.01
                or width / 2 > poly.bounds[2] * 1.01
        ):
            raise ValueError("Profile's width can not be larger than its contour lines."
                             "May be caused by critical overfilling.")

        polygon = clip_by_rect(poly, -width / 2, -math.inf, width / 2, math.inf)

        return cls(
            cross_section=polygon,
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

        return cls(
            cross_section=circle,
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
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        return cls(
            cross_section=polygon,
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
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        return cls(
            cross_section=polygon,
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
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        return cls(
            cross_section=polygon,
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
