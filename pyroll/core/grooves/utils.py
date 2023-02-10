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


def solve_box_like(
        r2: float,
        r4: float,
        depth: float,
        indent: float,
        ground_width: Optional[float],
        usable_width: Optional[float],
        flank_angle: Optional[float],
):
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
    even_ground_width = ground_width - 2 * ((r4 + r2) * np.sin(alpha4) + r2 * np.tan(flank_angle / 2))

    return dict(
        ground_width=ground_width,
        usable_width=usable_width,
        flank_angle=flank_angle,
        even_ground_width=even_ground_width,
        alpha4=alpha4
    )
