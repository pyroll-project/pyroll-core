import numpy as np

from ..generic_elongation import GenericElongationGroove
from scipy.optimize import root_scalar


class CircularOvalGroove(GenericElongationGroove):
    """Represents an oval-shaped groove with one main radius."""

    def __init__(self, r1: float, r2: float, depth: float, pad_angle: float = 0):
        """
        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param pad_angle: angle between z-axis and the roll face padding
        """
        pad_angle = np.deg2rad(pad_angle)

        def f(alpha):
            l23 = r1 * np.tan((alpha + pad_angle) / 2)
            return depth - r2 * (1 - np.cos(alpha)) - l23 * np.sin(alpha)

        alpha = root_scalar(f, bracket=(0, np.pi / 2)).root

        l23 = r1 * np.tan((alpha + pad_angle) / 2)
        usable_width = 2 * (l23 * np.cos(alpha) + r2 * np.sin(alpha))

        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=alpha,
            pad_angle=pad_angle
        )

    @property
    def types(self) -> '("oval", "circular_oval")':
        return "oval", "circular_oval"
