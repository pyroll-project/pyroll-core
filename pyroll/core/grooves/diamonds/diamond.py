from typing import Optional

import numpy as np
from numpy import deg2rad

from ..generic_elongation import GenericElongationGroove


class DiamondGroove(GenericElongationGroove):
    """Represent a diamond-shaped groove."""

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
        """
        if tip_angle is not None:
            tip_angle = np.deg2rad(tip_angle)

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

        self._tip_depth = tip_depth
        self._tip_angle = tip_angle

        depth = tip_depth - r2 / np.cos(alpha) + r2

        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=alpha, pad_angle=deg2rad(pad_angle)
        )

    @property
    def classifiers(self):
        return {"diamond", } | super().classifiers

    @property
    def tip_depth(self):
        """Depth of the intersection of the extrapolated flanks."""
        return self._tip_depth

    @property
    def tip_angle(self):
        """Angle between the flanks."""
        return self._tip_angle

    @property
    def __attrs__(self):
        return super().__attrs__ | dict(tip_depth=self.tip_depth, tip_angle=self.tip_angle)
