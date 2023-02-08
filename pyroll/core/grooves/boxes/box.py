from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove


class BoxGroove(GenericElongationGroove):
    """Represents a box-shaped groove."""

    def __init__(
            self,
            r1: float,
            r2: float,
            depth: float,
            ground_width: Optional[float] = None,
            usable_width: Optional[float] = None,
            flank_angle: Optional[float] = None
    ):
        """
        Exactly two of ground_width, usable_width and flank_angle must be given.
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param ground_width: width of the groove ground
        :param usable_width: usable width of the groove
        :param flank_angle: inclination angle of the flanks
        :raises ValueError: if not exactly two of ground_width, usable_width and flank_angle are given
        """
        if flank_angle is not None:
            flank_angle = np.deg2rad(flank_angle)

        if ground_width and usable_width and not flank_angle:
            flank_angle = np.arctan(depth / (usable_width - ground_width) * 2)
        elif usable_width and flank_angle and not ground_width:
            ground_width = usable_width - 2 * depth / np.tan(flank_angle)
        elif ground_width and flank_angle and not usable_width:
            usable_width = ground_width + 2 * depth / np.tan(flank_angle)
        else:
            raise ValueError(
                "Exactly two of the following arguments must be given: ground_width, usable_width, flank_angle must be given."
            )

        even_ground_width = ground_width - 2 * r2 * np.tan(flank_angle / 2)

        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=flank_angle,
            even_ground_width=even_ground_width
        )

    @property
    def types(self) -> '("box",)':
        return "box",
