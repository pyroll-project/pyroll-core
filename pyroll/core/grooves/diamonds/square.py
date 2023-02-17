from typing import Optional

import numpy as np

from .diamond import DiamondGroove


class SquareGroove(DiamondGroove):
    """Represents a square-shaped groove (diamond with tip angle near 90°)."""

    def __init__(
            self,
            r1: float,
            r2: float,
            usable_width: Optional[float] = None,
            tip_depth: Optional[float] = None,
            tip_angle: Optional[float] = None,
            pad_angle: float = 0
    ):
        """
        Exactly two of usable_width, tip_depth and tip_angle must be given.
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param usable_width: usable width of the groove
        :param tip_depth: depth of the intersection of the extrapolated flanks
        :param tip_angle: angle between the flanks
        :param pad_angle: angle between z-axis and the roll face padding
        :raises ValueError: if not exactly two of usable_width, tip_depth and tip_angle are given
        :raises ValueError: if tip angle is <85° or >95° (no matter if given or calculated internally)
        """

        super().__init__(
            r1=r1, r2=r2, usable_width=usable_width, tip_depth=tip_depth, tip_angle=tip_angle, pad_angle=pad_angle
        )

        tip_angle_deg = 180 - 2 * np.rad2deg(self.flank_angle)
        if tip_angle_deg > 95 or tip_angle_deg < 85:
            raise ValueError(
                "The tip angle of this SquareGroove significantly deviates from 90°, "
                "you should use a DiamondGroove instead."
            )

    @property
    def classifiers(self):
        return {"diamond", "square"} | super().classifiers
