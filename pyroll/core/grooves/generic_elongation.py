from typing import Union, Sequence, Optional

import numpy as np
from shapely.geometry import LineString, Polygon

from pyroll.core.grooves import GrooveBase
from pyroll.core.repr import ReprMixin
from ..config import Config


class GenericElongationGroove(GrooveBase, ReprMixin):
    """Represents a groove defined by the generic elongation groove geometry."""

    def __init__(
            self,

            r1: float,
            r2: float,

            flank_angle: Optional[float] = None,
            usable_width: Optional[float] = None,
            ground_width: Optional[float] = None,
            depth: Optional[float] = None,

            r3: float = 0,
            alpha3: float = 0,

            r4: float = 0,
            alpha4: float = 0,

            indent: float = 0,
            even_ground_width: float = 0,

            pad: float = 0,
            rel_pad: float = Config.GROOVE_PADDING,
            pad_angle: float = 0,

            classifiers: Sequence[str] = ()
    ):
        """
        Give any three of ``usable_width``, ``ground_width``, ``flank_angle`` and ``depth``.
        All angles are measured in radians.
        All measures must be non-negative.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/radius 3)

        :param usable_width: width of flank/face intersections
        :param ground_width: width of flank/ground-line intersections
        :param flank_angle: angle of the flanks to the z-axis
        :param depth: maximum depth

        :param r3: radius 3 (radius 2/radius 4)
        :param r4: radius 4 (radius 3/ground)
        :param alpha3: angle corresponding to ``r3``
        :param alpha4: angle corresponding to ``r4``


        :param indent: indent of the ground

        :param pad: absolute padding at roll face
        :param rel_pad: padding at roll face relative to ``usable_width``
        :param pad_angle: angle of the face padding from horizontal line
            (commonly 0 for two-roll, π/6 for three-roll and π/4 for four-roll)

        :param classifiers: sequence of additional type classifiers
        """

        mandatory_positive_or_zero = [r1, r2, r3, r4, alpha3, alpha4, indent, even_ground_width, flank_angle,
                                      usable_width, ground_width, depth]
        if not all(value is None or value >= 0 for value in mandatory_positive_or_zero):
            raise ValueError("Groove arguments have to be non-negative.")

        try:
            if usable_width is None:
                if np.isclose(depth, 0):
                    usable_width = ground_width
                else:
                    usable_width = ground_width + 2 * depth / np.tan(flank_angle)
            elif ground_width is None:
                if np.isclose(depth, 0):
                    ground_width = usable_width
                else:
                    ground_width = usable_width - 2 * depth / np.tan(flank_angle)
            elif flank_angle is None:
                flank_angle = np.arctan(depth / (usable_width - ground_width) * 2)
            elif depth is None:
                depth = (usable_width - ground_width) / 2 * np.tan(flank_angle)
            else:
                raise TypeError("Too many arguments given.")

        except TypeError:
            raise TypeError("Exactly three of usable_width, ground_width, flank_angle and depth must be given.")

        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4

        self.alpha1 = alpha1 = flank_angle + pad_angle
        self.alpha3 = alpha3
        self.alpha4 = alpha4
        self.alpha2 = alpha2 = flank_angle + self.alpha4 - self.alpha3

        self.indent = indent
        self.even_ground_width = even_ground_width
        self._usable_width = usable_width
        self.ground_width = ground_width
        self.flank_angle = flank_angle
        self._depth = depth
        self._classifiers = set(classifiers)
        pad = pad if pad else usable_width * rel_pad
        self.pad_angle = pad_angle

        self.z2 = usable_width / 2
        self.y2 = 0

        l12 = r1 * np.tan(alpha1 / 2)
        self.z1 = self.z2 + l12 * np.cos(pad_angle)
        self.y1 = l12 * np.sin(pad_angle)

        self.z0 = self.z1 + pad * np.cos(pad_angle)
        self.y0 = self.y1 + pad * np.sin(pad_angle)

        self.z12 = self.z1 - r1 * np.sin(pad_angle)
        self.y12 = self.y1 + r1 * np.cos(pad_angle)

        self.z3 = self.z12 - r1 * np.sin(flank_angle)
        self.y3 = self.y12 - r1 * np.cos(flank_angle)

        self.z9 = 0
        self.y9 = depth - indent

        self.z7 = self.even_ground_width / 2
        self.y7 = self.y9

        self.z8 = self.z7
        self.y8 = self.y9 + r4

        self.z6 = self.z8 + r4 * np.sin(alpha4)
        self.y6 = self.y8 - r4 * np.cos(alpha4)

        self.beta = beta = alpha4 - alpha3 / 2

        self.z10 = self.z6 + r3 * np.sin(alpha3 / 2 + beta)
        self.y10 = self.y6 - r3 * np.cos(alpha3 / 2 + beta)

        self.z5 = self.z10 + r3 * np.sin(alpha3 / 2 - beta)
        self.y5 = self.y10 + r3 * np.cos(alpha3 / 2 - beta)

        self.z11 = self.z10 + (r3 - r2) * np.sin(alpha3 / 2 - beta)
        self.y11 = self.y10 + (r3 - r2) * np.cos(alpha3 / 2 - beta)

        self.gamma = gamma = np.pi / 2 - alpha2 - alpha3 + alpha4

        self.z4 = self.z11 + r2 * np.cos(gamma)
        self.y4 = self.y11 + r2 * np.sin(gamma)

        right_side = np.array(list(self._enumerate_contour_points()))
        left_side = right_side[:-1].copy()
        left_side[:, 0] *= -1

        self._contour_points = np.concatenate([left_side, right_side[::-1]])
        self._contour_line = LineString(self._contour_points)
        self._cross_section = Polygon(self._contour_line)

        self.test_plausibility()
        self.test_complexity_of_contour_line()

    def _r1_contour_line(self, z):
        return self.y12 - np.sqrt(self.r1 ** 2 - (z - self.z12) ** 2)

    def _r2_contour_line(self, z):
        return self.y11 + np.sqrt(self.r2 ** 2 - (z - self.z11) ** 2)

    def _r3_contour_line(self, z):
        return self.y10 + np.sqrt(self.r3 ** 2 - (z - self.z10) ** 2)

    def _r4_contour_line(self, z):
        return self.y8 - np.sqrt(self.r4 ** 2 - (z - self.z8) ** 2)

    def _flank_contour_line(self, z):
        return self.y3 - np.tan(self.flank_angle) * (z - self.z3)

    def _ground_contour_line(self, z):
        return np.ones_like(z) * (self.depth - self.indent)

    @staticmethod
    def _face_contour_line(z):
        return np.zeros_like(z)

    def _enumerate_contour_points(self):
        yield self.z0, self.y0

        if not np.isclose(self.z1, self.z3):
            for z in np.linspace(self.z1, self.z3, Config.GROOVE_RADIUS_POINT_COUNT, endpoint=False):
                yield z, self._r1_contour_line(z)

        if not np.isclose(self.z3, self.z4):
            yield self.z3, self.y3

        if not np.isclose(self.z4, self.z5):
            for z in np.linspace(self.z4, self.z5, Config.GROOVE_RADIUS_POINT_COUNT, endpoint=False):
                yield z, self._r2_contour_line(z)

        if not np.isclose(self.z5, self.z6):
            for z in np.linspace(self.z5, self.z6, Config.GROOVE_RADIUS_POINT_COUNT, endpoint=False):
                yield z, self._r3_contour_line(z)

        if not np.isclose(self.z6, self.z7):
            for z in np.linspace(self.z6, self.z7, Config.GROOVE_RADIUS_POINT_COUNT, endpoint=False):
                yield z, self._r4_contour_line(z)

        yield self.z9, self.y9

    @property
    def contour_points(self):
        return self._contour_points

    @property
    def contour_line(self) -> LineString:
        return self._contour_line

    @property
    def cross_section(self) -> Polygon:
        return self._cross_section

    def local_depth(self, z) -> Union[float, np.ndarray]:
        z = np.abs(z)

        return np.piecewise(
            z,
            [z < self.z7, (self.z7 <= z) & (z < self.z6), (self.z6 <= z) & (z < self.z5),
             (self.z5 <= z) & (z < self.z4), (self.z4 <= z) & (z < self.z3), (self.z3 <= z) & (z < self.z1)],
            [self._ground_contour_line, self._r4_contour_line, self._r3_contour_line, self._r2_contour_line,
             self._flank_contour_line, self._r1_contour_line, self._face_contour_line]
        )

    @property
    def classifiers(self):
        return {"generic_elongation"} | self._classifiers

    @property
    def usable_width(self) -> float:
        return self._usable_width

    @property
    def width(self) -> float:
        return 2 * self.z1

    @property
    def depth(self) -> float:
        return self._depth

    def test_plausibility(self):
        if (self.flank_angle + self.alpha4 - self.alpha2 - self.alpha3) > 0.01:
            raise ValueError("given angles should fulfill α1 + α4 = α2 + α3 to be geometrically plausible")

        if self.y4 - self._flank_contour_line(self.z4) > 0.001 * self.depth:
            raise ValueError("under given conditions a step appears in z4")

    def test_complexity_of_contour_line(self):
        if not self.contour_line.is_simple:
            raise TypeError("Given groove arguments create complex contour line.")

    @property
    def __attrs__(self):
        return {
            n: v for n in ["r1", "r2", "r3", "r4", "alpha1", "alpha2", "alpha3", "alpha4", "depth", "indent",
                           "even_ground_width", "usable_width", "classifiers", "flank_angle", "pad_angle",
                           "ground_width",
                           "contour_line"]
            if (v := getattr(self, n))
        }
