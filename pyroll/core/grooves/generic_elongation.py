import logging
from typing import Union, Tuple

import numpy as np
from numpy import tan, sin, cos, pi, sqrt
from shapely.geometry import LineString, Polygon

from pyroll.core.grooves import GrooveBase


class GenericElongationGroove(GrooveBase):
    """Represents a groove defined by the generic elongation groove geometry."""

    def __init__(
            self,
            usable_width: float = 0,
            depth: float = 0,

            r1: float = 0,
            r2: float = 0,
            r3: float = 0,
            r4: float = 0,

            even_ground_width: float = 0,
            indent: float = 0,

            alpha1: float = 0,
            alpha2: float = 0,
            alpha3: float = 0,
            alpha4: float = 0,

            types: Tuple[str, ...] = ()
    ):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.alpha4 = alpha4
        self.indent = indent
        self.even_ground_width = even_ground_width
        self._usable_width = usable_width
        self._depth = depth
        self._types = types

        self._log = logging.getLogger(__name__)

        self.z2 = usable_width / 2
        self.y2 = 0

        self.z1 = self.z2 + r1 * tan(alpha1 / 2)
        self.y1 = 0

        self.z12 = self.z1
        self.y12 = r1

        self.z3 = self.z1 - r1 * sin(alpha1)
        self.y3 = r1 * (1 - cos(alpha1))

        self.z9 = 0
        self.y9 = depth - indent

        self.z7 = even_ground_width / 2
        self.y7 = self.y9

        self.z8 = self.z7
        self.y8 = self.y9 + r4

        self.z6 = self.z8 + r4 * sin(alpha4)
        self.y6 = self.y8 - r4 * cos(alpha4)

        self.beta = alpha4 - alpha3 / 2

        self.z10 = self.z6 + r3 * sin(alpha3 / 2 + self.beta)
        self.y10 = self.y6 - r3 * cos(alpha3 / 2 + self.beta)

        self.z5 = self.z10 + r3 * sin(alpha3 / 2 - self.beta)
        self.y5 = self.y10 + r3 * cos(alpha3 / 2 - self.beta)

        self.z11 = self.z10 + (r3 - r2) * sin(alpha3 / 2 - self.beta)
        self.y11 = self.y10 + (r3 - r2) * cos(alpha3 / 2 - self.beta)

        self.gamma = pi / 2 - alpha2 - alpha3 + alpha4

        self.z4 = self.z11 + r2 * cos(self.gamma)
        self.y4 = self.y11 + r2 * sin(self.gamma)

        right_side = np.unique(list(self._enumerate_contour_points()), axis=0)
        left_side = np.flip(right_side, axis=0).copy()
        left_side[:, 0] *= -1

        self._contour_line = LineString(np.concatenate([left_side, right_side]))
        self._cross_section = Polygon(self._contour_line)

        self.test_plausibility()

    def _r1_contour_line(self, z):
        return self.y12 - sqrt(self.r1 ** 2 - (z - self.z12) ** 2)

    def _r2_contour_line(self, z):
        return self.y11 + sqrt(self.r2 ** 2 - (z - self.z11) ** 2)

    def _r3_contour_line(self, z):
        return self.y10 + sqrt(self.r3 ** 2 - (z - self.z10) ** 2)

    def _r4_contour_line(self, z):
        return self.y8 - sqrt(self.r4 ** 2 - (z - self.z8) ** 2)

    def _flank_contour_line(self, z):
        return self.y3 - tan(self.alpha1) * (z - self.z3)

    def _ground_contour_line(self, z):
        return np.ones_like(z) * (self.depth - self.indent)

    @staticmethod
    def _face_contour_line(z):
        return np.zeros_like(z)

    def _enumerate_contour_points(self):
        yield 1.1 * self.z1, self.y1

        for z in np.linspace(self.z1, self.z3, 20):
            yield z, self._r1_contour_line(z)

        for z in np.linspace(self.z4, self.z5, 20):
            yield z, self._r2_contour_line(z)

        if not np.isclose(self.z5, self.z6):
            for z in np.linspace(self.z5, self.z6, 20):
                yield z, self._r3_contour_line(z)

        if not np.isclose(self.z6, self.z7):
            for z in np.linspace(self.z6, self.z7, 20):
                yield z, self._r4_contour_line(z)

        yield self.z9, self.y9

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
    def types(self) -> Tuple[str, ...]:
        return self._types

    @property
    def usable_width(self) -> float:
        return self._usable_width

    @property
    def depth(self) -> float:
        return self._depth

    def test_plausibility(self):
        if (self.alpha1 + self.alpha4 - self.alpha2 - self.alpha3) > 0.01:
            raise ValueError("given angles should fulfill α1 + α4 = α2 + α3 to be geometrically plausible")

        if self.y4 - self._flank_contour_line(self.z4) > 0.001 * self.y4:
            print(self.y4 - self._flank_contour_line(self.z4), 0.1 * self.y4)
            raise ValueError("under given conditions a step appears in z4")

    def _get_repr_attrs(self):
        return sorted(filter(
            lambda a: bool(getattr(self, a)),
            ["r1", "r2", "r3", "r4", "alpha1", "alpha2", "alpha3", "alpha4", "depth", "indent",
             "even_ground_width", "usable_width", "types"]
        ))

    def __repr__(self):
        return (
                type(self).__name__
                + "("
                + ", ".join(f"{attr}={getattr(self, attr)}" for attr in self._get_repr_attrs())
                + ")"
        )

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text(type(self).__name__ + "(...)")
            return

        with p.group(4, type(self).__name__ + "(", ")"):
            p.break_()
            for attr in self._get_repr_attrs():
                p.text(attr)
                p.text("=")
                p.pretty(getattr(self, attr))
                p.text(",")
                p.breakable()
