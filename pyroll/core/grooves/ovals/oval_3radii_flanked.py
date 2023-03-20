from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove
from ..generic_elongation_solvers import solve_r123


class Oval3RadiiFlankedGroove(GenericElongationGroove):
    """Represents an oval-shaped groove with 3 main radii and a dedicated flank."""

    def __init__(
            self,
            r1: float,
            r2: float,
            r3: float,
            depth: float,
            usable_width: float,
            flank_angle: Optional[float] = None,
            flank_width: Optional[float] = None,
            flank_height: Optional[float] = None,
            flank_length: Optional[float] = None,
            pad_angle: float = 0,
            **kwargs
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
        :param flank_width: horizontal extent of the flanks
        :param flank_height: vertical extent of the flanks
        :param flank_length: length of the flanks

        :param pad_angle: angle between z-axis and the roll face padding
        :param kwargs: more keyword arguments passed to the GenericElongationGroove constructor
        """

        if flank_angle is not None:
            flank_angle = np.deg2rad(flank_angle)

        pad_angle = np.deg2rad(pad_angle)

        sol = solve_r123(
            r1, r2, r3, depth, usable_width, pad_angle, flank_angle, flank_width, flank_height, flank_length
        )

        super().__init__(
            usable_width=usable_width, depth=depth,
            r1=r1, r2=r2, r3=r3,
            flank_angle=sol["flank_angle"], alpha3=sol["alpha3"], pad_angle=pad_angle,
            **kwargs
        )

    @property
    def classifiers(self):
        return {"oval", "oval_3_radii", "oval_3_radii_flanked"} | super().classifiers
