from typing import Optional
import numpy as np
from scipy.optimize import minimize, Bounds
from numpy import sin, cos, tan, pi, array
from ..generic_elongation import GenericElongationGroove


class Oval3RadiiGroove(GenericElongationGroove):
    """Represents an oval-shaped groove with 3 main radii."""

    def __init__(
            self,
            r1: float,
            r2: float,
            r3: float,
            depth: float,
            usable_width: float,
    ):
        """
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param r3: radius 3 (ground)
        :param depth: maximum depth
        :param usable_width: usable width of the groove
        """

        r32 = r3 - r2

        def half_outer_width(alpha1):
            return usable_width / 2 + r1 * tan(alpha1 / 2)

        def geometric_conditions(x):
            alpha2 = x[0]
            alpha3 = x[1]
            alpha1 = alpha2 + alpha3
            gamma = pi / 2 - alpha2 - alpha3
            return array((
                r1 * sin(alpha1) + r2 * cos(gamma) + r32 * sin(alpha3) - half_outer_width(alpha1),
                r1 * (1 - cos(alpha1)) - r2 * sin(gamma) - r32 * cos(alpha3) + r3 - depth
            ))

        sol = minimize(lambda x: np.sum(geometric_conditions(x) ** 2, axis=0), array([pi / 4, pi / 4]),
                       bounds=Bounds(0, pi / 2), tol=1e-8 * depth)

        if not sol.success:
            raise RuntimeError("Could not determine geometric values with given input.")

        alpha2 = sol.x[0]
        alpha3 = sol.x[1]
        alpha1 = alpha2 + alpha3

        super().__init__(
            usable_width=usable_width, depth=depth,
            r1=r1, r2=r2, r3=r3,
            flank_angle=alpha1, alpha3=alpha3
        )

    @property
    def types(self) -> '("oval", "oval_3_radii")':
        return "oval", "oval_3_radii"
