import numpy as np

from .base import OvalGrooveBase


class CircularOvalGroove(OvalGrooveBase):

    def __init__(self, r1: float, r2: float, depth: float):
        alpha = np.arccos(1 - depth / (r1 + r2))
        usable_width = 2 * (r1 * np.sin(alpha) + r2 * np.sin(alpha) - r1 * np.tan(alpha / 2))

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha)

        self.bachtinow_shternov_first_radius_test(lower_bound=0.07, upper_bound=0.08, dependent_value=self.depth)

    def __str__(self):
        return 'CircularOvalGroove {}'.format(self.groove_label)
