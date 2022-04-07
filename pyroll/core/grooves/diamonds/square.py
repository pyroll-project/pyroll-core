from typing import Optional

import numpy as np

from .diamond import DiamondGroove


class SquareGroove(DiamondGroove):
    """Represents a square shaped groove (diamond with tip angle near 90°)."""

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
        :raises ValueError: if tip angle is <85° or >95° (no matter if given or calculated internally)
        """

        super().__init__(r1=r1, r2=r2, usable_width=usable_width, tip_depth=tip_depth, tip_angle=tip_angle)

        tip_angle_deg = 180 - 2 * self.alpha1 / np.pi * 180
        if tip_angle_deg > 95 or tip_angle_deg < 85:
            raise ValueError(
                "The tip angle of this SquareGroove significantly deviates from 90°, "
                "you should use a DiamondGroove instead."
            )

    @property
    def types(self) -> '("diamond", "square")':
        return "diamond", "square"
