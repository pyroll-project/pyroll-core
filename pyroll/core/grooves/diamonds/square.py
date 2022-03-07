from typing import Optional

import numpy as np

from .diamond import DiamondGroove

class SquareGroove(DiamondGroove):

    def __init__(self, r1: float, r2: float, usable_width: Optional[float] = None, tip_depth: Optional[float] = None,
                 tip_angle: Optional[float] = None):
        super().__init__(r1=r1, r2=r2, usable_width=usable_width, tip_depth=tip_depth, tip_angle=tip_angle)

        self.bachtinow_shternov_second_radius_test(lower_bound=0.07, upper_bound=0.08, dependent_value=self.depth)

        tip_angle_deg = 180 - 2 * self.alpha1 / np.pi * 180
        if tip_angle_deg > 95 or tip_angle_deg < 85:
            raise ValueError(
                "The tip angle of this SquareGroove significantly deviates from 90°, you should use a DiamondGroove instead.")

    def __str__(self):
        return 'SquareGroove {}'.format(self.groove_label)
