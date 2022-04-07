import numpy as np

from ..generic_elongation import GenericElongationGroove


class FlatOvalGroove(GenericElongationGroove):
    """Represent an oval shaped groove with a flat ground."""

    def __init__(self, r1: float, r2: float, depth: float, usable_width: float):
        """
        :param r1: radius of the first edge
        :type r1: float
        :param r2: radius of the second edge
        :type r2: float
        :param depth: depth of the groove
        :type depth: float
        :param usable_width:  ground width excluding influence of radii
        :type usable_width: float
        """
        alpha = np.arccos(1 - depth / (r1 + r2))
        even_ground_width = usable_width - 2 * (r1 * np.sin(alpha) + r2 * np.sin(alpha) - r1 * np.tan(alpha / 2))

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha,
                         even_ground_width=even_ground_width)

    @property
    def types(self) -> '("oval", "flat_oval")':
        return "oval", "flat_oval"
