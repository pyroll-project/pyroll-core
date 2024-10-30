import math
from typing import Optional, Union, Callable
from collections.abc import Set

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import Point, LinearRing, Polygon, LineString
from shapely.ops import clip_by_rect

from ..config import Config
from ..grooves import GrooveBase
from ..hooks import HookHost, Hook


class Profile(HookHost):
    """Represents a profile aka a workpiece state."""

    cross_section = Hook[Polygon]()
    """Shape of the profile's cross-section."""

    technologically_orientated_cross_section = Hook[Polygon]()
    """Shape of the profile's cross-section with technologically correct orientation."""

    classifiers = Hook[Set[str]]()
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

    equivalent_radius = Hook[float]()
    """Radius of a equivalent round."""

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

    flow_stress_function = Hook[Callable[[float, float, float], float]]()
    """Flow stress depended on strain, strain-rate and temperature"""

    elastic_modulus = Hook[float]()
    """Mean elastic modulus of the profile material."""

    poissons_ratio = Hook[float]()
    """Mean Poisson's ratio of the profile material."""

    thermal_conductivity = Hook[float]()
    """Mean thermal conductivity of the profile material."""

    specific_heat_capacity = Hook[float]()
    """Mean specific heat capacity of the profile material."""

    density = Hook[float]()
    """Mean density (specific weight) of the profile material."""

    material = Hook[Union[str, Set[str]]]()
    """String or sequence of strings classifying the material of the profile.
    Can be used by material databases to retrieve respective data."""

    grain_size = Hook[float]()
    """Average grain size of the profile's material."""

    astm_grain_size_number = Hook[float]()
    """ASTM grain size number, assuming grains are round."""

    heat_penetration_number = Hook[float]()
    """Mean heat penetration number of the profile material."""

    thermal_diffusivity = Hook[float]()
    """Mean thermal diffusivity of the profile material."""

    chemical_composition = Hook[dict[str, float]]()
    """Chemical composition of the profile's material as dict of element symbols to atom fractions (0 to 1).
    The key of the dict should correspond to the nomenclature of the TDB (Thermodynamic Data Base file). 
    This means only capital letters and abbreviations according to the periodic table of the elements."""

    microstructure_composition = Hook[dict[str, float]]()
    """Phase resp. constituent composition of the profile's material 
    as dict of constituent names to volume fractions (0 to 1)."""

    scale_thickness = Hook[float]()
    """Thickness of the scale covering the profile."""

    longitudinal_stress = Hook[float]()
    """Normal stress (principal stress) in rolling (x) direction. Positive means tension, negative pressure."""

    altitudinal_stress = Hook[float]()
    """Normal stress (principal stress) in thickness (y) direction. Positive means tension, negative pressure."""

    latitudinal_stress = Hook[float]()
    """Normal stress (principal stress) in width (z) direction. Positive means tension, negative pressure."""

    longitudinal_strain = Hook[float]()
    """Logarithmic normal strain (principal strain) in rolling (x) direction."""

    altitudinal_strain = Hook[float]()
    """Logarithmic normal strain (principal strain) in thickness (y) direction."""

    latitudinal_strain = Hook[float]()
    """Logarithmic normal strain (principal strain) in width (z) direction."""

    hydrostatic_stress = Hook[float]()
    """Hydrodynamic Stress."""

    equivalent_stress = Hook[float]()
    """Equivalent Stress."""

    normal_stress = Hook[float]()
    """Normal Stress acting between profile and tooling."""

    longitudinal_contact_friction = Hook[float]()
    """Contact friction between profile and tooling in rolling (x) direction."""

    latitudinal_contact_friction = Hook[float]()
    """Contact friction between profile and tooling in width (z) direction."""

    deformation_activation_energy = Hook[float]()
    """Activation energy of deformation especially for calculation of Zener-Holomon-Parameter."""

    martensite_start_temperature = Hook[float]()
    """Martensite start temperature for the given chemical composition of the profile."""

    martensite_finish_temperature = Hook[float]()
    """Martensite finish temperature for the given chemical composition of the profile."""

    bainite_start_temperature = Hook[float]()
    """Bainite start temperature for the given chemical composition of the profile."""

    bainite_finish_temperature = Hook[float]()
    """Bainite finish temperature for the given chemical composition of the profile."""

    ae1_temperature = Hook[float]()
    """Temperature at which austenite starts to transform into a mixture of ferrite and cementite during cooling."""

    ae3_temperature = Hook[float]()
    """Temperature above which the transformation of austenite into a mixture of ferrite and cementite is complete during cooling."""

    vickers_hardness = Hook[float]()
    """Vickers hardness of the cold profile material."""

    def __init__(self, **kwargs):
        """Using the ``__init__`` is not recommended, use one of the factory class methods instead."""
        self.t = 0
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
            # noinspection PyUnresolvedReferences
            cls.logger.warning("Encountered overfilled groove in profile construction.")

        upper_contour_line = translate(groove.contour_line, yoff=gap / 2)
        lower_contour_line = rotate(upper_contour_line, angle=180, origin=(0, 0))

        poly = Polygon(
            np.concatenate(
                [
                    upper_contour_line.coords,
                    lower_contour_line.coords
                ]
            )
        )

        if (
                # one percent tolerance to bypass discretization issues
                - width / 2 < poly.bounds[0] * 1.01
                or width / 2 > poly.bounds[2] * 1.01
        ):
            raise ValueError(
                "Profile's width can not be larger than its contour lines."
                "May be caused by critical overfilling."
            )

        polygon = clip_by_rect(poly, -width / 2, -math.inf, width / 2, math.inf)

        return cls(
            cross_section=refine_cross_section(polygon),
            classifiers=set(groove.classifiers),
            **kwargs
        )

    @classmethod
    def from_polygon(
            cls,
            cross_section: Polygon,
            classifiers: Set[str],
            **kwargs
    ) -> 'Profile':
        """
        Creates a custom profile from a shapely polygon object.

        :param cross_section: a polygon representing the cross-section shape
        :param classifiers: a set of strings classifying the shape
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        """

        if not cross_section.is_simple:
            raise ValueError("The cross-section must be a simple polygon.")

        if not cross_section.is_valid:
            raise ValueError("The cross-section must be a valid polygon.")

        if cross_section.is_empty:
            raise ValueError("The cross-section must not be empty.")

        if len(cross_section.interiors) > 0:
            raise ValueError("The cross-section must not contain holes.")

        return cls(
            cross_section=cross_section,
            classifiers=set(classifiers),
            **kwargs
        )

    @classmethod
    def round(
            cls,
            radius: Optional[float] = None,
            diameter: Optional[float] = None,
            **kwargs
    ) -> 'RoundProfile':
        """
        Creates a round shaped profile (a real circle round, without imperfections of round grooves).
        Give exactly one of ``radius`` and ``diameter``.

        :param radius: the radius of the round profile, must be > 0
        :param diameter: the diameter of the round profile, must be > 0
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises TypeError: on invalid argument combinations
        :raises ValueError: if arguments are out of range
        """

        return RoundProfile(radius, diameter, **kwargs)

    @classmethod
    def square(
            cls,
            side: Optional[float] = None,
            diagonal: Optional[float] = None,
            corner_radius: float = 0,
            **kwargs
    ) -> 'SquareProfile':
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

        return SquareProfile(side, diagonal, corner_radius, **kwargs)

    @classmethod
    def box(
            cls,
            height: float,
            width: float,
            corner_radius: float = 0,
            **kwargs
    ) -> 'BoxProfile':
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

        return BoxProfile(height, width, corner_radius, **kwargs)

    @classmethod
    def diamond(
            cls,
            height: float,
            width: float,
            corner_radius: float = 0,
            **kwargs
    ) -> 'DiamondProfile':
        """
        Creates a diamond shaped profile (a real diamond shape with rounded corners,
        without imperfections of diamond grooves).
        A diamond is oriented to stand on its corner.

        :param height: the height of the diamond profile, must be > 0
        :param width: the width of the diamond profile, must be > 0
        :param corner_radius: the radius of the diamond's corners, must be >= 0, <= height / 2 and <= width / 2
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises ValueError: if arguments are out of range
        """

        return DiamondProfile(height, width, corner_radius, **kwargs)

    @classmethod
    def hexagon(
            cls,
            side: Optional[float] = None,
            height: Optional[float] = None,
            diagonal: Optional[float] = None,
            corner_radius: float = 0,
            **kwargs
    ) -> 'HexagonProfile':
        """
        Creates a hexagonal shaped profile (a real hexagonal shape with rounded corners,
        without imperfections of hexagonal grooves). A hexagon is oriented to stand on its side.
        Give exactly one of ``side``, ``height`` and ``diagonal``.

        :param side: the side length of the hexagonal profile, must be > 0
        :param height: the height of the hexagonal profile when standing on the flat base, must be > 0
        :param diagonal: the diagonal length of the hexagonal profile (corner-to-corner distance)
        :param corner_radius: the radius of the hexagon's corners, must be >= 0, <= diagonal / 2
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises TypeError: on invalid argument combinations
        :raises ValueError: if arguments are out of range
        """

        return HexagonProfile(side, height, diagonal, corner_radius, **kwargs)

    def local_height(self, z: float) -> float:
        coords = np.array([(1, -1), (1, 1)]) * (z, self.height)

        vline = LineString(
            coords
        )

        tolerance = 1e-12

        intersection = vline.intersection(self.cross_section.buffer(tolerance))

        return intersection.length

    def local_width(self, y: float) -> float:
        coords = np.array([(-1, 1), (1, 1)]) * (self.width, y)

        hline = LineString(
            coords
        )

        tolerance = 1e-12

        intersection = hline.intersection(self.cross_section.buffer(tolerance))

        return intersection.length

    def fits_material(self, key: str):
        """Return true, if the given material key is present in the profile's material hook (case-insensitive),
        otherwise false."""

        def _format(s):
            try:
                return s.lower()
            except AttributeError:
                raise ValueError(f"Given value {repr(s)} is no str.")

        key = _format(key)

        try:
            return key in _format(self.material)

        except ValueError:
            try:
                return key in {
                    _format(k)
                    for k in self.material
                }
            except TypeError:
                raise ValueError("Value of self.material is neither a string or a collection of strings.")

    def _plot_matplotlib_(self):
        import matplotlib.pyplot as plt

        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()

        ax.set_ylabel("y")
        ax.set_xlabel("z")

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        ax.plot(*self.cross_section.boundary.xy, color="k")
        ax.fill(*self.cross_section.boundary.xy, color="k", alpha=0.5)
        return fig

    def _plot_plotly_(self):
        import plotly.express as px

        fig = px.line(
            x=self.cross_section.boundary.xy[0],
            y=self.cross_section.boundary.xy[1],
            labels={"y": "y", "x": "z"},
        )

        fig.data[0].fill = "toself"

        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1
        )

        return fig


class RoundProfile(Profile):
    def __init__(
            self,
            radius: Optional[float] = None,
            diameter: Optional[float] = None,
            **kwargs
    ):
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

        self._radius = radius
        self._diameter = diameter

        center = Point((0, 0))
        circle = center.buffer(radius)

        super().__init__(
            cross_section=refine_cross_section(circle),
            classifiers={"round"},
            **kwargs
        )

    @property
    def radius(self):
        """The radius of the round shaped profile (half diameter)."""
        return self._radius

    @property
    def diameter(self):
        """The diameter of the round shaped profile (double radius)."""
        return self._diameter

    @property
    def __attrs__(self):
        return super().__attrs__ | dict(radius=self.radius, diameter=self.diameter)


class BoxProfile(Profile):
    def __init__(
            self,
            height: float,
            width: float,
            corner_radius: float = 0,
            **kwargs
    ):
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

        self._corner_radius = corner_radius

        line = LinearRing(
            np.array([(1, -1), (1, 1), (-1, 1), (-1, -1)])
            * (width / 2 - corner_radius, height / 2 - corner_radius)
        )
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        super().__init__(
            cross_section=refine_cross_section(polygon),
            classifiers={"box"},
            **kwargs
        )

    @property
    def corner_radius(self):
        """The radius of the profile's corners resp. edges."""
        return self._corner_radius

    @property
    def __attrs__(self):
        return super().__attrs__ | dict(corner_radius=self._corner_radius)


class DiamondProfile(Profile):
    def __init__(
            self,
            height: float,
            width: float,
            corner_radius: float = 0,
            **kwargs
    ):
        """
        Creates a diamond shaped profile (a real diamond shape with rounded corners,
        without imperfections of diamond grooves).
        A diamond is oriented to stand on its corner.

        :param height: the height of the diamond profile, must be > 0
        :param width: the width of the diamond profile, must be > 0
        :param corner_radius: the radius of the diamond's corners, must be >= 0, <= height / 2 and <= width / 2
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

        self._corner_radius = corner_radius

        line = LinearRing(
            np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])
            * (width / 2 - corner_radius, height / 2 - corner_radius)
        )
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        super().__init__(
            cross_section=refine_cross_section(polygon),
            classifiers={"diamond"},
            **kwargs
        )

    @property
    def corner_radius(self):
        """The radius of the profile's corners resp. edges."""
        return self._corner_radius

    @property
    def __attrs__(self):
        return super().__attrs__ | dict(corner_radius=self._corner_radius)


class SquareProfile(Profile):
    def __init__(
            self,
            side: Optional[float] = None,
            diagonal: Optional[float] = None,
            corner_radius: float = 0,
            **kwargs
    ):
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

        self._side = side
        self._diagonal = diagonal
        self._corner_radius = corner_radius

        line = LinearRing(np.array([(1, 0), (0, 1), (-1, 0), (0, -1)]) * (diagonal / 2 - corner_radius * np.sqrt(2)))
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        super().__init__(
            cross_section=refine_cross_section(polygon),
            classifiers={"square", "diamond"},
            **kwargs
        )

    @property
    def side(self):
        """The side length of the square profile."""
        return self._side

    @property
    def diagonal(self):
        """The diagonal length of the profile."""
        return self._diagonal

    @property
    def corner_radius(self):
        """The radius of the profile's corners resp. edges."""
        return self._corner_radius

    @property
    def __attrs__(self):
        return super().__attrs__ | dict(
            side=self._side,
            diagonal=self._diagonal,
            corner_radius=self._corner_radius
        )


class HexagonProfile(Profile):
    def __init__(
            self,
            side: Optional[float] = None,
            height: Optional[float] = None,
            diagonal: Optional[float] = None,
            corner_radius: float = 0,
            **kwargs
    ):
        """
        Creates a hexagonal shaped profile (a real hexagonal shape with rounded corners,
        without imperfections of hexagonal grooves). A hexagon is oriented to stand on its side.
        Give exactly one of ``side``, ``height`` and ``diagonal``.

        :param side: the side length of the hexagonal profile, must be > 0
        :param height: the height of the hexagonal profile when standing on the flat base, must be > 0
        :param diagonal: the diagonal length of the hexagonal profile (corner-to-corner distance)
        :param corner_radius: the radius of the hexagon's corners, must be >= 0, <= diagonal / 2
        :param kwargs: additional keyword arguments to be passed to the Profile constructor
        :raises TypeError: on invalid argument combinations
        :raises ValueError: if arguments are out of range
        """

        if side is not None and diagonal is None and height is None:
            height = side * np.sqrt(3)
            diagonal = side * 2
        elif diagonal is not None and side is None and height is None:
            side = diagonal / 2
            height = side / np.sqrt(3)
        elif height is not None and side is None and diagonal is None:
            side = height / np.sqrt(3)
            diagonal = side * 2
        else:
            raise TypeError("either 'side', 'height' or 'diagonal' must be given")

        if (
                side <= 0
                or height <= 0
                or diagonal <= 0
                or corner_radius < 0
                or corner_radius > side / 2
        ):
            raise ValueError("argument value(s) out of range")

        self._corner_radius = corner_radius
        self._side = side
        self._diagonal = diagonal

        line = LinearRing(
            np.array([
                (-1, 0),
                (-1 / 2, np.sqrt(3) / 2),
                (1 / 2, np.sqrt(3) / 2),
                (1, 0),
                (1 / 2, -np.sqrt(3) / 2),
                (-1 / 2, -np.sqrt(3) / 2),
            ])
            * (side, side)
        )
        polygon = Polygon(line)
        polygon = polygon.buffer(corner_radius)

        super().__init__(
            cross_section=refine_cross_section(polygon),
            classifiers={"hexagon"},
            **kwargs
        )

    @property
    def side(self):
        """The side length of the hexagon profile."""
        return self._side

    @property
    def diagonal(self):
        """The diagonal between two flat sides of the hexagon profile."""
        return self._diagonal

    @property
    def corner_radius(self):
        """The radius of the profile's corners resp. edges."""
        return self._corner_radius

    @property
    def __attrs__(self):
        return super().__attrs__ | dict(
            side=self._side,
            diagonal=self._diagonal,
            corner_radius=self._corner_radius)


def refine_cross_section(cross_section: Polygon):
    if Config.PROFILE_CONTOUR_REFINEMENT < 1:
        return cross_section

    return cross_section.segmentize(cross_section.boundary.length / Config.PROFILE_CONTOUR_REFINEMENT)
