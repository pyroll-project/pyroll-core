import numpy as np
from ..generic_elongation import GenericElongationGroove
from ..utils import solve_three_radii


class UpsetOvalGroove(GenericElongationGroove):
    """Represents an upright oval-shaped groove."""

    def __init__(
            self,
            r1: float,
            r2: float,
            r3: float,
            depth: float,
            usable_width: float,
            pad_angle: float = 0
    ):
        """
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param r3: radius 3 (ground)
        :param depth: maximum depth
        :param usable_width: usable width of the groove
        :param pad_angle: angle between z-axis and the roll face padding
        """

        pad_angle = np.deg2rad(pad_angle)

        sol = solve_three_radii(r1, r2, r3, depth, usable_width, pad_angle)

        if sol["flank_angle"] > np.pi / 2:
            raise ValueError("under the given conditions the flank angle is > 90°")

        super().__init__(
            usable_width=usable_width, depth=depth,
            r1=r1, r2=r2, r3=r3,
            flank_angle=sol["flank_angle"], alpha3=sol["alpha3"], pad_angle=pad_angle
        )

    @property
    def types(self) -> '("oval", "oval_3_radii")':
        return "oval", "upset"
