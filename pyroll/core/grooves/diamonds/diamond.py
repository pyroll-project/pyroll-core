from typing import Optional

import numpy as np

from .base import DiamondGrooveBase


class DiamondGroove(DiamondGrooveBase):

    def __init__(self, r1: float, r2: float,
                 usable_width: Optional[float] = None,
                 tip_depth: Optional[float] = None,
                 tip_angle: Optional[float] = None
                 ):
        if usable_width and tip_depth and not tip_angle:
            alpha = np.arctan(tip_depth / (usable_width / 2))

        elif usable_width and tip_angle and not tip_depth:
            alpha = np.pi / 2 - tip_angle / 2
            tip_depth = usable_width / 2 * np.tan(alpha)

        elif tip_depth and tip_angle and not usable_width:
            alpha = np.pi / 2 - tip_angle / 2
            usable_width = tip_depth / np.tan(alpha) * 2
        else:
            raise ValueError("Exactly two of the following arguments must be given: usable_width, tip_depth, tip_angle")

        depth = tip_depth - r2 / np.cos(alpha) + r2

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha)

        self.bachtinow_shternov_first_radius_test(lower_bound=0.8, upper_bound=1.0, dependent_value=self.r1)
        self.bachtinow_shternov_second_radius_test(lower_bound=0.08, upper_bound=1.0, dependent_value=tip_depth)

    def __str__(self):
        return 'DiamondGroove {}'.format(self.groove_label)
