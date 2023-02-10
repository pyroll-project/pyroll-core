from typing import Optional

import numpy as np
from scipy.optimize import root_scalar, minimize_scalar


def solve_two_radii(
        r1: float,

        r2: Optional[float],
        depth: Optional[float],
        width: Optional[float],

        pad_angle: float,

        flank_angle: Optional[float] = None,
        flank_width: Optional[float] = None,
        flank_height: Optional[float] = None,
        flank_length: Optional[float] = None,
):
    def l23(_alpha):
        return r1 * np.tan((_alpha + pad_angle) / 2)

    if flank_angle is None:
        if flank_length is not None:
            def fw(_alpha):
                return flank_length * np.cos(_alpha)

            def fh(_alpha):
                return flank_length * np.sin(_alpha)

        elif flank_width is not None:
            def fw(_alpha):
                return flank_width

            def fh(_alpha):
                return flank_width * np.tan(_alpha)

        elif flank_height is not None:
            def fw(_alpha):
                return flank_height / np.tan(_alpha)

            def fh(_alpha):
                return flank_height

        else:
            def fw(_alpha):
                return 0

            def fh(_alpha):
                return 0

        if width is None:
            def f(_alpha):
                return depth - r2 * (1 - np.cos(_alpha)) - l23(_alpha) * np.sin(_alpha) - fh(_alpha)

            flank_angle = root_scalar(f, bracket=(0, np.pi / 2)).root

        elif depth is None:
            def f(_alpha):
                return width / 2 - r2 * np.sin(_alpha) - l23(_alpha) * np.cos(_alpha) - fw(_alpha)

            raster = np.linspace(0, np.pi / 2, 100)
            values = f(raster)
            lower = raster[values > 0][0]
            upper = raster[values < 0][-1]
            flank_angle = root_scalar(f, bracket=(lower, upper)).root

        elif r2 is None:
            def f(_alpha):
                return (
                        width / 2
                        - (depth - l23(_alpha) * np.sin(_alpha) - fh(_alpha)) / (1 - np.cos(_alpha)) * np.sin(_alpha)
                        - l23(_alpha) * np.cos(_alpha) - fw(_alpha)
                )

            flank_angle = root_scalar(f, bracket=(0, np.pi / 2)).root

        else:
            raise TypeError("Give either usable_width or depth.")

    if width is None:
        width = 2 * (
                l23(flank_angle) * np.cos(flank_angle) + r2 * np.sin(flank_angle)
                + (
                        depth - r2 * (1 - np.cos(flank_angle)) - l23(flank_angle) * np.sin(flank_angle)
                ) / np.tan(flank_angle)
        )

    elif depth is None:
        depth = (
                r2 * (1 - np.cos(flank_angle))
                + (width / 2 - r2 * np.sin(flank_angle))
                * np.tan(flank_angle)
        )

    elif r2 is None:
        r2 = (
                (depth - width / 2 * np.tan(flank_angle))
                / (1 - np.cos(flank_angle) - np.sin(flank_angle) * np.tan(flank_angle))
        )

    else:
        raise TypeError("Give either usable_width or depth.")

    return dict(
        width=width,
        depth=depth,
        r2=r2,
        alpha=flank_angle,
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
