import numpy as np

from .base import RoundGrooveBase


class FalseRoundGroove(RoundGrooveBase):
    def __init__(self, r1: float, r2: float,depth: float,flank_angle: float):
        tip_depth = depth + r2 / np.cos(flank_angle) - r2
        usable_width = tip_depth / np.tan(flank_angle) * 2

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=flank_angle, alpha2=flank_angle)

    def __str__(self):
        return 'FalseRoundGroove {}'.format(self.groove_label)
