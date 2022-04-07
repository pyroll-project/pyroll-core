from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove


class DiamondGroove(GenericElongationGroove):
    """Represent a diamond shaped groove."""

    def __init__(
            self,
            r1: float,
            r2: float,
            usable_width: Optional[float] = None,
            tip_depth: Optional[float] = None,
            tip_angle: Optional[float] = None
    ):
        """
        Exactly two of usable_width, tip_depth and tip_angle must be given.

        :param r1: radius of the first edge
        :type r1: float
        :param r2: radius of the second edge
        :type r2: float
        :param usable_width:  ground width excluding influence of radii
        :type usable_width: float
        :param tip_depth: depth of the tip of the groove
        :type tip_depth: float
        :param tip_angle: angle at witch the tip is formed
        :type tip_angle: float
        :raises ValueError: if not exactly two of usable_width, tip_depth and tip_angle are given
        """

        if usable_width and tip_depth and not tip_angle:
            alpha = np.arctan(tip_depth / (usable_width / 2))

        elif usable_width and tip_angle and not tip_depth:
            alpha = np.pi / 2 - tip_angle / 2
            tip_depth = usable_width / 2 * np.tan(alpha)

        elif tip_depth and tip_angle and not usable_width:
            alpha = np.pi / 2 - tip_angle / 2
            usable_width = tip_depth / np.tan(alpha) * 2
        else:
            raise ValueError(
                "Exactly two of the following arguments must be given: usable_width, tip_depth, tip_angle."
            )

        depth = tip_depth - r2 / np.cos(alpha) + r2

        super().__init__(usable_width=usable_width, depth=depth, r1=r1, r2=r2, alpha1=alpha, alpha2=alpha)

    @property
    def types(self) -> '("diamond",)':
        return "diamond",
