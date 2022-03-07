from typing import Optional
import numpy as np
from .base import OvalGrooveBase
from scipy.optimize import minimize, Bounds
from numpy import sin, cos, tan, pi, array


class Oval3RadiiGroove(OvalGrooveBase):

    def __init__(
            self,
            r1: float,
            r2: float,
            r3: float,
            depth: float,
            usable_width: float,
    ):
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
            alpha1=alpha1, alpha2=alpha2, alpha3=alpha3
        )

    def __str__(self):
        return 'Oval3Radii {}'.format(self.groove_label)
