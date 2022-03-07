import numpy as np

from .base import RoundGrooveBase


class RoundGroove(RoundGrooveBase):

    def __init__(self, r1: float, r2: float, depth: float):
        alpha = np.arccos(1 - depth / (r1 + r2))
        usable_width = 2 * (r1 * np.sin(alpha) + r2 * np.sin(alpha) - r1 * np.tan(alpha / 2))

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha)

        self.bachtinow_shternov_first_radius_test(lower_bound=0.06, upper_bound=0.08, dependent_value=self.depth)
        self.bachtinow_shternov_second_radius_test(lower_bound=1, upper_bound=1, dependent_value=self.depth / 2)

    def __str__(self):
        return 'RoundGroove {}'.format(self.groove_label)
