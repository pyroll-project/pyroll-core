from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove
from ..generic_elongation_solvers import solve_r124


class FalseRoundGroove(GenericElongationGroove):
    """Represents a round-shaped groove with a dedicated flank (false round)."""

    def __init__(
            self,
            r1: float,

            r2: Optional[float] = None,
            depth: Optional[float] = None,
            usable_width: Optional[float] = None,

            flank_angle: Optional[float] = None,
            flank_width: Optional[float] = None,
            flank_height: Optional[float] = None,
            flank_length: Optional[float] = None,

            pad_angle: float = 0,
            **kwargs
    ):
        """
        All angles are measured in ° (degree).
        Give exactly two of ``r2``, ``depth`` or ``usable_width``.
        Give exactly one of ``flank_angle``, ``flank_width``, ``flank_height`` or ``flank_length``.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width

        :param flank_angle: inclination angle of the flanks
        :param flank_width: horizontal extent of the flanks
        :param flank_height: vertical extent of the flanks
        :param flank_length: length of the flanks
        :param pad_angle: angle between z-axis and the roll face padding
        :param kwargs: more keyword arguments passed to the GenericElongationGroove constructor
        """
        pad_angle = np.deg2rad(pad_angle)

        if flank_angle is not None:
            flank_angle = np.deg2rad(flank_angle)

        sol = solve_r124(
            r1=r1,
            r2=r2, depth=depth, width=usable_width,
            pad_angle=pad_angle,
            flank_angle=flank_angle, flank_width=flank_width, flank_height=flank_height, flank_length=flank_length
        )

        super().__init__(
            r2=sol["r2"], depth=sol["depth"], usable_width=sol["width"], flank_angle=sol["alpha"],
            r1=r1, pad_angle=pad_angle,
            **kwargs
        )

    @property
    def classifiers(self):
        return {"round", "false_round"} | super().classifiers
