import numpy as np

from ..generic_elongation import GenericElongationGroove


class RoundGroove(GenericElongationGroove):
    """Represents a round-shaped groove."""

    def __init__(self, r1: float, r2: float, depth: float):
        """
        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        """

        alpha = np.arccos(1 - depth / (r1 + r2))
        usable_width = 2 * (r1 * np.sin(alpha) + r2 * np.sin(alpha) - r1 * np.tan(alpha / 2))

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha)

    @property
    def types(self) -> '("round",)':
        return "round",
