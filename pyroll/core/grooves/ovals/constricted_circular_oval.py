import numpy as np

from ..generic_elongation import GenericElongationGroove
from ..generic_elongation_solvers import solve_r1234


class ConstrictedCircularOvalGroove(GenericElongationGroove):
    """Represents an oval-shaped groove with one main radius."""

    def __init__(
            self,
            r1: float,
            r2: float,
            r3: float,
            r4: float,
            depth: float,
            usable_width: float,
            indent: float,
            even_ground_width: float = 0,
            pad_angle: float = 0,
            **kwargs
    ):
        """
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param r3: radius 3 (ground)
        :param r4: radius 4 (indent)
        :param depth: maximum depth
        :param usable_width: usable width of the groove
        :param even_ground_width: width of the even ground line
        :param pad_angle: angle between z-axis and the roll face padding
        :param kwargs: more keyword arguments passed to the GenericElongationGroove constructor
        """

        pad_angle = np.deg2rad(pad_angle)

        sol = solve_r1234(r1, r2, r3, r4, depth, usable_width - even_ground_width, indent, pad_angle)

        super().__init__(
            usable_width=usable_width, depth=depth, indent=indent,
            even_ground_width=even_ground_width,
            r1=r1, r2=r2, r3=r3, r4=r4,
            flank_angle=sol["flank_angle"], alpha3=sol["alpha3"], alpha4=sol["alpha4"], pad_angle=pad_angle,
            **kwargs
        )

    @property
    def classifiers(self):
        return {"oval", "circular_oval", "constricted"} | super().classifiers
