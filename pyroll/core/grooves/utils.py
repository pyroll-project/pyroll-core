from typing import Optional

import numpy as np
from scipy.optimize import root_scalar, minimize_scalar


def solve_two_radii(
        r1: float,
        r2: Optional[float],
        depth: Optional[float],
        width: Optional[float],
        pad_angle: float,
        sol_index: int,
):
    def l23(_alpha):
        return r1 * np.tan((_alpha + pad_angle) / 2)

    if width is None:
        def f(_alpha):
            return depth - r2 * (1 - np.cos(_alpha)) - l23(_alpha) * np.sin(_alpha)

        alpha = root_scalar(f, bracket=(0, np.pi / 2)).root
        width = 2 * (l23(alpha) * np.cos(alpha) + r2 * np.sin(alpha))
    elif depth is None:
        def f(_alpha):
            return width / 2 - r2 * np.sin(_alpha) - l23(_alpha) * np.cos(_alpha)

        if r2 * 2 <= width:
            m = minimize_scalar(f, bracket=(0, np.pi / 2)).x
            alphas = root_scalar(f, bracket=(0, m)).root, root_scalar(f, bracket=(m, np.pi / 2)).root
            alpha = alphas[sol_index]
        else:
            alpha = root_scalar(f, bracket=(0, np.pi / 2)).root

        depth = l23(alpha) * np.sin(alpha) + r2 * (1 - np.cos(alpha))
    elif r2 is None:
        def f(_alpha):
            return width / 2 - (depth - l23(_alpha) * np.sin(_alpha)) / (1 - np.cos(_alpha)) * np.sin(
                _alpha
            ) - l23(_alpha) * np.cos(_alpha)

        alpha = root_scalar(f, bracket=(0, np.pi / 2)).root
        r2 = (depth - l23(alpha) * np.sin(alpha)) / (1 - np.cos(alpha))

    else:
        raise TypeError("Give either usable_width or depth.")

    return dict(
        width=width,
        depth=depth,
        r2=r2,
        alpha=alpha,
    )
