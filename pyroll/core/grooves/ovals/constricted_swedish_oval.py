from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove
from ..generic_elongation_solvers import solve_box_like


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
            even_ground_width: Optional[float] = None,
            usable_width: Optional[float] = None,
            flank_angle: Optional[float] = None,
            pad_angle: float = 0,
            **kwargs
    ):
        """
        Exactly two of ``ground_width``, ``even_ground_width``, ``usable_width`` and ``flank_angle`` must be given,
        but not ``ground_width`` and ``even_ground_width`` at the same time.
        Widths are always measured at the intersection of the extrapolated ground, face and flanks.
        All angles are measured in ° (degree).

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank)
        :param r4: radius 4 (indent)
        :param depth: maximum depth
        :param indent: depth of the indent
        :param ground_width: width of the groove ground
        :param even_ground_width: width of the even ground line
        :param usable_width: usable width of the groove
        :param flank_angle: inclination angle of the flanks
        :param pad_angle: angle between z-axis and the roll face padding
        :param kwargs: more keyword arguments passed to the GenericElongationGroove constructor
        :raises ValueError: if not exactly two of ground_width, usable_width and flank_angle are given
        """
        if flank_angle is not None:
            flank_angle = np.deg2rad(flank_angle)

        sol = solve_box_like(
            r2=r2, r4=r4, depth=depth, ground_width=ground_width, usable_width=usable_width, flank_angle=flank_angle,
            indent=indent, even_ground_width=even_ground_width
        )

        super().__init__(
            r1=r1, r2=r2, r4=r4, pad_angle=np.deg2rad(pad_angle), indent=indent,
            **sol,
            **kwargs
        )

    @property
    def classifiers(self):
        return {"oval", "swedish_oval", "constricted_swedish_oval"} | super().classifiers
