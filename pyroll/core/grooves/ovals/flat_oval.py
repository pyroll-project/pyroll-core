from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove
from ..utils import solve_two_radii


class FlatOvalGroove(GenericElongationGroove):
    """Represent an oval-shaped groove with a flat ground."""

    def __init__(
            self,
            r1: float,
            r2: float,
            depth: float,
            usable_width: float,
            pad_angle: float = 0,
    ):
        """
        Give exactly two of ``r2``, ``depth`` or ``usable_width``.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width
        :param pad_angle: angle between z-axis and the roll face padding
        """
        pad_angle = np.deg2rad(pad_angle)

        sol = solve_two_radii(r1=r1, r2=r2, depth=depth, width=None, pad_angle=pad_angle, sol_index=0)

        super().__init__(
            r2=sol["r2"], depth=sol["depth"], usable_width=usable_width, flank_angle=sol["alpha"],
            even_ground_width=usable_width - sol["width"],
            r1=r1, pad_angle=pad_angle
        )

    @property
    def types(self) -> '("oval", "flat_oval")':
        return "oval", "flat_oval"
