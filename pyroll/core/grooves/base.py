import logging
from dataclasses import dataclass
from typing import Optional, List

import numpy as np
from numpy import tan, sin, cos, pi, sqrt
from scipy.integrate import quad

@dataclass
class GrooveBase:
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

        self.cross_section = 2 * quad(self.contour_line, 0, self.z1)[0]
        self.mean_depth = (self.cross_section / (2 * self.z1))
        self.mean_width = (self.cross_section / self.depth)

        self._log = logging.getLogger(__name__)

        self.test_plausibility()

    def contour_line(self, z: float) -> np.piecewise:
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        z = np.abs(z)

        return np.piecewise(
            z,
            [z < self.z7, (self.z7 <= z) & (z < self.z6), (self.z6 <= z) & (z < self.z5),
             (self.z5 <= z) & (z < self.z4), (self.z4 <= z) & (z < self.z3), (self.z3 <= z) & (z < self.z1)],
            [self.ground_contour_line, self.r4_contour_line, self.r3_contour_line, self.r2_contour_line,
             self.flank_contour_line, self.r1_contour_line, self.face_contour_line]
        )

    def r1_contour_line(self, z):
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        return self.y12 - sqrt(self.r1 ** 2 - (z - self.z12) ** 2)

    def r2_contour_line(self, z):
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        return self.y11 + sqrt(self.r2 ** 2 - (z - self.z11) ** 2)

    def r3_contour_line(self, z):
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        return self.y10 + sqrt(self.r3 ** 2 - (z - self.z10) ** 2)

    def r4_contour_line(self, z):
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        return self.y8 - sqrt(self.r4 ** 2 - (z - self.z8) ** 2)

    def flank_contour_line(self, z):
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        return self.y3 - tan(self.alpha1) * (z - self.z3)

    def ground_contour_line(self, z):
        """

        :param z:
        :type z:
        :return:
        :rtype:
        """
        return np.ones_like(z) * (self.depth - self.indent)

    @staticmethod
    def face_contour_line(z):
        return np.zeros_like(z)

    def contour_derivative(self, z):
        abs_z = np.abs(z)

        derivatives = np.piecewise(
            abs_z,
            [abs_z < self.z7, (self.z7 <= abs_z) & (abs_z < self.z6), (self.z6 <= abs_z) & (abs_z < self.z5),
             (self.z5 <= abs_z) & (abs_z < self.z4), (self.z4 <= abs_z) & (abs_z < self.z3),
             (self.z3 <= abs_z) & (abs_z < self.z1)],
            [self.ground_contour_derivative, self.r4_contour_derivative, self.r3_contour_derivative,
             self.r2_contour_derivative,
             self.flank_contour_derivative, self.r1_contour_derivative, self.face_contour_derivative]
        )

        return np.piecewise(
            z,
            [z >= 0, z < 0],
            [derivatives, -derivatives]
        )

    def r1_contour_derivative(self, z):
        return (z - self.z12) / sqrt(self.r1 ** 2 - (z - self.z12) ** 2)

    def r2_contour_derivative(self, z):
        return -(z - self.z11) / sqrt(self.r2 ** 2 - (z - self.z11) ** 2)

    def r3_contour_derivative(self, z):
        return -(z - self.z10) / sqrt(self.r3 ** 2 - (z - self.z10) ** 2)

    def r4_contour_derivative(self, z):
        return (z - self.z8) / sqrt(self.r4 ** 2 - (z - self.z8) ** 2)

    def flank_contour_derivative(self, z):
        return -tan(self.alpha1) * np.ones_like(z)

    @staticmethod
    def ground_contour_derivative(z):
        return np.zeros_like(z)

    @staticmethod
    def face_contour_derivative(z):
        return np.zeros_like(z)

    def bachtinow_shternov_first_radius_test(self, lower_bound: float, upper_bound: float, dependent_value: float):

        if self.r1 < lower_bound * dependent_value or self.r1 > upper_bound * dependent_value:
            self._log.warning('Groove %s first radius outside recommended values!' % self.__str__())

    def bachtinow_shternov_second_radius_test(self, lower_bound: float, upper_bound: float, dependent_value: float):

        if self.r2 < lower_bound * dependent_value or self.r2 > upper_bound * dependent_value:
            self._log.warning('Groove %s second radius outside recommended values!' % self.__str__())

    def test_plausibility(self):
        if (self.alpha1 + self.alpha4 - self.alpha2 - self.alpha3) > 0.01:
            raise ValueError("given angles should fulfill α1 + α4 = α2 + α3 to be geometrically plausible")

        if self.y4 - self.flank_contour_line(self.z4) > 0.001 * self.y4:
            print(self.y4 - self.flank_contour_line(self.z4), 0.1 * self.y4)
            raise ValueError("under given conditions a step appears in z4")
