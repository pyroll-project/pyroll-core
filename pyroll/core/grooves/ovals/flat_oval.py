import numpy as np

from ..generic_elongation import GenericElongationGroove


class FlatOvalGroove(GenericElongationGroove):
    """Represent an oval-shaped groove with a flat ground."""

    def __init__(self, r1: float, r2: float, depth: float, usable_width: float):
        """
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width of the groove
        """
        alpha = np.arccos(1 - depth / (r1 + r2))
        even_ground_width = usable_width - 2 * (r1 * np.sin(alpha) + r2 * np.sin(alpha) - r1 * np.tan(alpha / 2))

        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=alpha,
            even_ground_width=even_ground_width
            )

    @property
    def types(self) -> '("oval", "flat_oval")':
        return "oval", "flat_oval"
