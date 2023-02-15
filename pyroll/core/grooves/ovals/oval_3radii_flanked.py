from typing import Optional

import numpy as np
from scipy.optimize import brentq
from numpy import sin, cos, tan, pi

from ..generic_elongation import GenericElongationGroove


class Oval3RadiiFlankedGroove(GenericElongationGroove):
    """Represents an oval-shaped groove with 3 main radii and a dedicated flank."""

    def __init__(
            self,
            r1: float,
            r2: float,
            r3: float,
            depth: float,
            usable_width: float,
            flank_angle: float,
    ):
        """
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param r3: radius 3 (ground)
        :param depth: maximum depth
        :param usable_width: usable width of the groove
        :param flank_angle: inclination angle of the flanks
        """

        alpha1 = np.deg2rad(flank_angle)
        r32 = r3 - r2
        gamma = pi / 2 - alpha1

        half_outer_width = usable_width / 2 + r1 * tan(alpha1 / 2)

        def geometric_conditions(alpha2):
            alpha3 = alpha1 - alpha2
            delta_w = r1 * sin(alpha1) + r2 * cos(gamma) + r32 * sin(alpha3) - half_outer_width
            delta_t = r1 * (1 - cos(alpha1)) - r2 * sin(gamma) - r32 * cos(alpha3) + r3 - depth
            flank_length = (delta_w - delta_t) / (sin(alpha1) - cos(alpha1))

            return delta_t + flank_length * sin(alpha1)

        try:
            sol = brentq(geometric_conditions, 0, alpha1)
        except:
            raise RuntimeError("Could not determine geometric values with given input.")

        alpha2 = sol
        alpha3 = alpha1 - alpha2

        super().__init__(
            usable_width=usable_width, depth=depth,
            r1=r1, r2=r2, r3=r3,
            alpha1=alpha1, alpha2=alpha2, alpha3=alpha3
        )

    @property
    def types(self) -> '("oval", "oval_3_radii", "oval_3_radii_flanked")':
        return "oval", "oval_3_radii", "oval_3_radii_flanked"
