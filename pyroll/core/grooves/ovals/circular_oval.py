from typing import Optional

import numpy as np

from ..generic_elongation import GenericElongationGroove
from scipy.optimize import root_scalar


class CircularOvalGroove(GenericElongationGroove):
    """Represents an oval-shaped groove with one main radius."""

    def __init__(
            self,
            r1: float,
            r2: float,
            depth: Optional[float] = None,
            usable_width: Optional[float] = None,
            pad_angle: float = 0
    ):
        """
        Give either ``depth`` or ``usable_width``.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width
        :param pad_angle: angle between z-axis and the roll face padding
        """
        pad_angle = np.deg2rad(pad_angle)

        def l23(_alpha):
            return r1 * np.tan((_alpha + pad_angle) / 2)

        if usable_width is None:
            def f(_alpha):
                return depth - r2 * (1 - np.cos(_alpha)) - l23(_alpha) * np.sin(_alpha)

            alpha = root_scalar(f, bracket=(0, np.pi / 2)).root
            usable_width = 2 * (l23(alpha) * np.cos(alpha) + r2 * np.sin(alpha))
        elif depth is None:
            def f(_alpha):
                return usable_width / 2 - r2 * np.sin(_alpha) - l23(_alpha) * np.cos(_alpha)

            alpha = root_scalar(f, bracket=(0, np.pi / 2)).root
            depth = l23(alpha) * np.sin(alpha) + r2 * (1 - np.cos(alpha))

        else:
            raise TypeError("Give either usable_width or depth.")

        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=alpha,
            pad_angle=pad_angle
        )

    @property
    def types(self) -> '("oval", "circular_oval")':
        return "oval", "circular_oval"
