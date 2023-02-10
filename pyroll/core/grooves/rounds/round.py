from typing import Optional

import numpy as np
from scipy.optimize import root_scalar, minimize_scalar

from ..generic_elongation import GenericElongationGroove


class RoundGroove(GenericElongationGroove):
    """Represents a round-shaped groove."""

    def __init__(
            self,
            r1: float,
            r2: float,
            depth: Optional[float] = None,
            usable_width: Optional[float] = None,
            pad_angle: float = 0,
            sol_index: int = 0,
    ):
        """
        Give either ``depth`` or ``usable_width``.

        :param r1: radius 1 (face/flank)
        :param r2: radius 2 (flank/ground)
        :param depth: maximum depth
        :param usable_width: usable width
        :param pad_angle: angle between z-axis and the roll face padding
        :param sol_index: If ``r2`` and ``usable_width`` are given there may be two valid solutions if ``2 * r2 < usable_width``.
                Specify this index to choose one.
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

            if r2 * 2 <= usable_width:
                m = minimize_scalar(f, bracket=(0, np.pi / 2)).x
                alphas = root_scalar(f, bracket=(0, m)).root, root_scalar(f, bracket=(m, np.pi / 2)).root
                alpha = alphas[sol_index]
            else:
                alpha = root_scalar(f, bracket=(0, np.pi / 2)).root

            depth = l23(alpha) * np.sin(alpha) + r2 * (1 - np.cos(alpha))
        elif r2 is None:
            def f(_alpha):
                return usable_width / 2 - (depth - l23(_alpha) * np.sin(_alpha)) / (1 - np.cos(_alpha)) * np.sin(
                    _alpha
                ) - l23(_alpha) * np.cos(_alpha)

            alpha = root_scalar(f, bracket=(0, np.pi / 2)).root
            r2 = (depth - l23(alpha) * np.sin(alpha)) / (1 - np.cos(alpha))

        else:
            raise TypeError("Give either usable_width or depth.")

        super().__init__(
            usable_width=usable_width, depth=depth, r1=r1, r2=r2, flank_angle=alpha,
            pad_angle=pad_angle
        )

    @property
    def types(self) -> '("round",)':
        return "round",
