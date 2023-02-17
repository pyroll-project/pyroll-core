import numpy as np
from ..generic_elongation import GenericElongationGroove
from ..generic_elongation_solvers import solve_r123


class GothicGroove(GenericElongationGroove):
    """Represents a square-shaped groove with curved flanks similar to a gothic arc."""

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

        sol = solve_r123(r1, r2, r3, depth, usable_width, pad_angle)

        super().__init__(
            usable_width=usable_width, depth=depth,
            r1=r1, r2=r2, r3=r3,
            flank_angle=sol["flank_angle"], alpha3=sol["alpha3"], pad_angle=pad_angle
        )

    @property
    def classifiers(self):
        return {"diamond", "square", "gothic"} | super().classifiers
