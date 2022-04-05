import numpy as np

from .base import OvalGrooveBase


class FlatOvalGroove(OvalGrooveBase):
    def __init__(self, r1: float, r2: float, depth: float, usable_width: float):
        alpha = np.arccos(1 - depth / (r1 + r2))
        even_ground_width = usable_width - 2 * (r1 * np.sin(alpha) + r2 * np.sin(alpha) - r1 * np.tan(alpha / 2))

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha,
                         even_ground_width=even_ground_width)

    @property
    def types(self):
        return super().types + ("flat_oval",)
