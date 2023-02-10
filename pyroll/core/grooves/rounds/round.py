from typing import Optional

import numpy as np
from scipy.optimize import root_scalar, minimize_scalar

from ..generic_elongation import GenericElongationGroove
from ..utils import solve_two_radii


class RoundGroove(GenericElongationGroove):
    """Represents a round-shaped groove."""

    def __init__(
            self,
            r1: float,
            r2: Optional[float] = None,
            depth: Optional[float] = None,
            usable_width: Optional[float] = None,
            pad_angle: float = 0,
            sol_index: int = 0,
    ):
        """
        Give exactly two of ``r2``, ``depth`` or ``usable_width``.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width
        :param pad_angle: angle between z-axis and the roll face padding
        :param sol_index: If ``r2`` and ``usable_width`` are given there may be two valid solutions if ``2 * r2 < usable_width``.
                Specify this index to choose one.
        """
        pad_angle = np.deg2rad(pad_angle)

        sol = solve_two_radii(r1=r1, r2=r2, depth=depth, width=usable_width, pad_angle=pad_angle, sol_index=sol_index)

        super().__init__(
            r2=sol["r2"], depth=sol["depth"], usable_width=sol["width"], flank_angle=sol["alpha"],
            r1=r1, pad_angle=pad_angle
        )

    @property
    def types(self) -> '("round",)':
        return "round",
