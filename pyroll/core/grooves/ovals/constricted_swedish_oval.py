from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove


class ConstrictedSwedishOvalGroove(GenericElongationGroove):
    """Represents a hexagonal-shaped groove with an indented ground that is used like an oval groove (swedish oval)."""

    def __init__(
            self,
            r1: float,
            r2: float,
            r4: float,
            depth: float,
            indent: float,
            ground_width: Optional[float] = None,
            usable_width: Optional[float] = None,
            flank_angle: Optional[float] = None
    ):
        """
        Exactly two of ground_width, usable_width and flank_angle must be given.
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank)
        :param r4: radius 4 (indent)
        :param depth: maximum depth
        :param indent: depth of the indent
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
                "Exactly two of the following arguments must be given: ground_width, usable_width, flank_angle."
            )

        alpha4 = np.arccos(1 - indent / (r2 + r4))
        alpha2 = flank_angle + alpha4
        even_ground_width = ground_width - 2 * ((r4 + r2) * np.sin(alpha4) + r2 * np.tan(flank_angle / 2))

        super().__init__(
            usable_width=usable_width, depth=depth,
            r1=r1, r2=r2, r3=r2, r4=r4,
            alpha1=flank_angle, alpha2=alpha2, alpha4=alpha4,
            even_ground_width=even_ground_width, indent=indent
        )

    @property
    def types(self) -> '("oval", "swedish_oval", "constricted_swedish_oval")':
        return "oval", "swedish_oval", "constricted_swedish_oval"
