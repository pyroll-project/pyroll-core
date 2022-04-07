import numpy as np

from ..generic_elongation import GenericElongationGroove


class FalseRoundGroove(GenericElongationGroove):
    """Represents a round shaped groove with a dedicated flank (false round)."""

    def __init__(self, r1: float, r2: float, depth: float, flank_angle: float):
        """
        :param r1: radius of the first edge
        :type r1: float
        :param r2: radius of the second edge
        :type r2: float
        :param depth: depth of the groove
        :type depth: float
        :param flank_angle: angle of the flanks
        :type flank_angle: float
        """

        tip_depth = depth + r2 / np.cos(flank_angle) - r2
        usable_width = tip_depth / np.tan(flank_angle) * 2

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=flank_angle, alpha2=flank_angle)

    @property
    def types(self) -> '("round", "false_round")':
        return "round", "false_round"
