from typing import Optional

import numpy as np
from numpy import deg2rad

from ..generic_angle import GenericAngleGroove
from ..generic_elongation_solvers import solve_r124

__all__ = ["PreformingGroove"]


class PreformingGroove(GenericAngleGroove):
    """Represent a diamond-shaped groove."""

    def __init__(
        self,
        r1: float,
        r2: float,
        usable_width: Optional[float] = None,
        inner_width: Optional[float] = None,
        tip_depth: Optional[float] = None,
        tip_angle: Optional[float] = None,
        pad_angle: float = 0,
    ):
        """
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param usable_width: usable width of the groove
        :param inner_width: width of the inner forming part of the groove
        :param tip_depth: depth of the intersection of the extrapolated flanks
        :param tip_angle: angle between the flanks
        :param pad_angle: angle between z-axis and the roll face padding
        :raises ValueError: if not exactly two of usable_width, tip_depth and tip_angle are given
        """
        if tip_angle is not None:
            tip_angle = np.deg2rad(tip_angle)
            alpha = np.pi / 2 - tip_angle / 2
            inner_width = tip_depth / np.tan(alpha) * 2
            depth = tip_depth - r2 / np.cos(alpha) + r2
            self._tip_angle = tip_angle


        else:
            sol = solve_r124(r1=r1, r2=r2, depth=tip_depth, width=inner_width, pad_angle=pad_angle)
            r2 = sol["r2"]
            depth = sol["depth"]
            inner_width = sol["width"]
            alpha = sol["alpha"]
            r1 = r1


        self._tip_depth = tip_depth


        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=alpha, pad_angle=deg2rad(pad_angle),
            inner_usable_width=inner_width
        )


    @property
    def classifiers(self):
        return {
            "edge",
        } | super().classifiers

    @property
    def depth(self):
        """Depth of the intersection of the extrapolated flanks."""
        return self._tip_depth


    @property
    def __attrs__(self):
        return super().__attrs__ | dict(tip_depth=self.depth)
