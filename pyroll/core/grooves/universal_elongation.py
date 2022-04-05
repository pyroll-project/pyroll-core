import logging
from abc import ABC
from dataclasses import dataclass
from typing import Optional, Union

import numpy as np
from numpy import tan, sin, cos, pi, sqrt
from scipy.integrate import quad
from shapely.geometry import LineString, Polygon

from pyroll.core.grooves import GrooveBase


@dataclass
class UniversalElongationGroove(GrooveBase, ABC):
    usable_width: float = 0
    depth: float = 0

    r1: float = 0
    r2: float = 0
    r3: float = 0
    r4: float = 0

    even_ground_width: float = 0
    indent: float = 0

    alpha1: float = 0
    alpha2: float = 0
    alpha3: float = 0
    alpha4: float = 0

    groove_label: Optional[str] = ""

    def __post_init__(self):
        self._log = logging.getLogger(__name__)

        self.z2 = self.usable_width / 2
        self.y2 = 0

        self.z1 = self.z2 + self.r1 * tan(self.alpha1 / 2)
        self.y1 = 0

        self.z12 = self.z1
        self.y12 = self.r1

        self.z3 = self.z1 - self.r1 * sin(self.alpha1)
        self.y3 = self.r1 * (1 - cos(self.alpha1))

        self.z9 = 0
        self.y9 = self.depth - self.indent

        self.z7 = self.even_ground_width / 2
        self.y7 = self.y9

        self.z8 = self.z7
        self.y8 = self.y9 + self.r4

        self.z6 = self.z8 + self.r4 * sin(self.alpha4)
        self.y6 = self.y8 - self.r4 * cos(self.alpha4)

        self.beta = self.alpha4 - self.alpha3 / 2

        self.z10 = self.z6 + self.r3 * sin(self.alpha3 / 2 + self.beta)
        self.y10 = self.y6 - self.r3 * cos(self.alpha3 / 2 + self.beta)

        self.z5 = self.z10 + self.r3 * sin(self.alpha3 / 2 - self.beta)
        self.y5 = self.y10 + self.r3 * cos(self.alpha3 / 2 - self.beta)

        self.z11 = self.z10 + (self.r3 - self.r2) * sin(self.alpha3 / 2 - self.beta)
        self.y11 = self.y10 + (self.r3 - self.r2) * cos(self.alpha3 / 2 - self.beta)

        self.gamma = pi / 2 - self.alpha2 - self.alpha3 + self.alpha4

        self.z4 = self.z11 + self.r2 * cos(self.gamma)
        self.y4 = self.y11 + self.r2 * sin(self.gamma)

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

    def test_plausibility(self):
        if (self.alpha1 + self.alpha4 - self.alpha2 - self.alpha3) > 0.01:
            raise ValueError("given angles should fulfill α1 + α4 = α2 + α3 to be geometrically plausible")

        if self.y4 - self._flank_contour_line(self.z4) > 0.001 * self.y4:
            print(self.y4 - self._flank_contour_line(self.z4), 0.1 * self.y4)
            raise ValueError("under given conditions a step appears in z4")
