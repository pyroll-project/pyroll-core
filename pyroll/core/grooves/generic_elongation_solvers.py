from typing import Optional

import numpy as np
from scipy.optimize import root_scalar, root, fixed_point


# angle brackets for numerical solvers to prevent divide by zero
MIN_ANGLE = 1e-6
MAX_ANGLE = np.pi / 2 - MIN_ANGLE


def solve_r124(
        r1: float,

        r2: Optional[float],
        depth: Optional[float],
        width: Optional[float],

        pad_angle: float,

        flank_angle: Optional[float] = None,
        flank_width: Optional[float] = None,
        flank_height: Optional[float] = None,
        flank_length: Optional[float] = None,

        r4: float = 0,
        indent: float = 0,
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

            flank_angle = root_scalar(f, bracket=(MIN_ANGLE, MAX_ANGLE)).root

        elif depth is None:
            alpha4 = np.arccos(1 - indent / (r2 + r4))

            def f(_alpha):
                return (
                        width / 2 - r2 * np.sin(_alpha) - l23(_alpha) * np.cos(_alpha)
                        - fw(_alpha) - (r2 + r4) * np.sin(alpha4)
                )

            raster = np.linspace(MIN_ANGLE, MAX_ANGLE, 100)
            values = f(raster)
            lower = raster[values > 0][0]
            upper = raster[values < 0][-1]
            flank_angle = root_scalar(f, bracket=(lower, upper)).root

        elif r2 is None:
            def f(_alpha):
                _r2 = (depth - l23(_alpha) * np.sin(_alpha) - fh(_alpha)) / (1 - np.cos(_alpha))
                _alpha4 = np.arccos(1 - indent / (_r2 + r4))

                return (
                        width / 2 - _r2 * np.sin(_alpha) - l23(_alpha) * np.cos(_alpha)
                        - fw(_alpha) - (_r2 + r4) * np.sin(_alpha4)
                )

            flank_angle = root_scalar(f, bracket=(MIN_ANGLE, MAX_ANGLE)).root

        else:
            raise TypeError("Give either usable_width or depth.")

    if r2 is not None:
        alpha4 = np.arccos(1 - indent / (r2 + r4))

        if width is None:
            width = 2 * (
                    r2 * np.sin(flank_angle)
                    + (depth - r2 * (1 - np.cos(flank_angle))) / np.tan(flank_angle)
                    + (r2 + r4) * np.sin(alpha4)
            )

        elif depth is None:
            depth = (
                    r2 * (1 - np.cos(flank_angle))
                    + (width / 2 - r2 * np.sin(flank_angle) - (r2 + r4) * np.sin(alpha4)) * np.tan(flank_angle)
            )

    else:
        def f(_r2):
            _alpha4 = np.arccos(1 - indent / (_r2 + r4))
            return (
                    (depth - width / 2 * np.tan(flank_angle) + r4 * np.sin(_alpha4))
                    / (1 - np.cos(flank_angle) - np.sin(flank_angle) * np.tan(flank_angle) - np.sin(_alpha4))
            )

        r2 = fixed_point(f, width if width > depth else depth)
        alpha4 = np.arccos(1 - indent / (r2 + r4))

    return dict(
        width=width,
        depth=depth,
        r2=r2,
        alpha=flank_angle,
    )


def solve_r123(
        r1: float,
        r2: float,
        r3: float,
        depth: float,
        width: float,

        pad_angle: float,

        flank_angle: Optional[float] = None,
        flank_width: Optional[float] = None,
        flank_height: Optional[float] = None,
        flank_length: Optional[float] = None,
):
    def l23(_alpha):
        return r1 * np.tan((_alpha + pad_angle) / 2)

    r32 = r3 - r2

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

        def f(_alpha):
            _alpha2 = _alpha[0]
            _alpha3 = _alpha[1]
            _flank_angle = _alpha2 + _alpha3
            _gamma = np.pi / 2 - _flank_angle

            return np.array(
                [
                    (
                            depth - r3 + r32 * np.cos(_alpha3) + r2 * np.sin(_gamma)
                            - fh(_flank_angle) - l23(_flank_angle) * np.sin(_flank_angle)
                    ),
                    (
                            width / 2 - r32 * np.sin(_alpha3) - r2 * np.cos(_gamma)
                            - fw(_flank_angle) - l23(_flank_angle) * np.cos(_flank_angle)
                    ),
                ]
            )

        sol = root(
            f, np.array([np.pi / 4, np.pi / 4]),
        )

        if not sol.success:
            raise RuntimeError("Could not determine geometric values with given input.")

        alpha2 = sol.x[0]
        alpha3 = sol.x[1]
        flank_angle = alpha2 + alpha3

    else:
        def f(_alpha):
            _alpha2 = _alpha
            _alpha3 = flank_angle - _alpha
            _gamma = np.pi / 2 - flank_angle

            _fw = width / 2 - r32 * np.sin(_alpha3) - r2 * np.cos(_gamma) - l23(flank_angle) * np.cos(flank_angle)

            return (
                    depth - r3 + r32 * np.cos(_alpha3) + r2 * np.sin(_gamma)
                    - _fw * np.tan(flank_angle) - l23(flank_angle) * np.sin(flank_angle)
            )

        sol = root_scalar(f, bracket=(MIN_ANGLE, MAX_ANGLE)).root
        alpha2 = sol
        alpha3 = flank_angle - sol

    return dict(
        flank_angle=flank_angle,
        alpha2=alpha2,
        alpha3=alpha3,
    )


def solve_r1234(
        r1: float,
        r2: float,
        r3: float,
        r4: float,
        depth: float,
        width: float,
        indent: float,

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

        def f(_alpha):
            _alpha2 = _alpha[0]
            _alpha3 = _alpha[1]
            _alpha4 = _alpha[2]
            _flank_angle = _alpha2 + _alpha3 - _alpha4

            if _alpha3 > _alpha4:
                _gamma = np.pi / 2 - _flank_angle
                return np.array(
                    [
                        (
                                depth - r3 + (r3 - r2) * np.cos(_alpha3 - _alpha4) + r2 * np.sin(_gamma)
                                - fh(_flank_angle) - l23(_flank_angle) * np.sin(_flank_angle)
                        ),
                        (
                                width / 2 - (r3 - r2) * np.sin(_alpha3 - _alpha4) - r2 * np.cos(_gamma)
                                - fw(_flank_angle) - l23(_flank_angle) * np.cos(_flank_angle)
                                - (r3 + r4) * np.sin(_alpha4)
                        ),
                        (
                                indent - (r3 + r4) * (1 - np.cos(_alpha4))
                        )
                    ]
                )
            else:
                _gamma = np.pi / 2 - _alpha4
                return np.array(
                    [
                        (
                                depth - r2 * (1 - np.cos(_flank_angle))
                                - fh(_flank_angle) - l23(_flank_angle) * np.sin(_flank_angle)
                        ),
                        (
                                width / 2 - r2 * np.sin(_flank_angle)
                                - fw(_flank_angle) - l23(_flank_angle) * np.cos(_flank_angle)
                                - r4 * np.sin(_alpha4) - r3 * np.cos(_gamma)
                                - (r2 - r3) * np.sin(_alpha2 - _flank_angle)
                        ),
                        (
                                indent - r4 * (1 - np.cos(_alpha4)) + r3 * np.sin(_gamma)
                                + (r2 - r3) * np.cos(_alpha4 - _alpha3) - r2
                        )
                    ]
                )

        sol = root(
            f, np.array([np.pi / 4, np.pi / 4, np.pi / 4]),
        )

        if not sol.success:
            raise RuntimeError("Could not determine geometric values with given input.")

        alpha2 = sol.x[0]
        alpha3 = sol.x[1]
        alpha4 = sol.x[2]
        flank_angle = alpha2 + alpha3 - alpha4

    else:
        def f(_alpha):
            _alpha2 = _alpha[0]
            _alpha3 = _alpha[1]
            _alpha4 = _alpha2 + _alpha3 - flank_angle
            _gamma = np.pi / 2 - flank_angle

            _fw = width / 2 - (r3 - r2) * np.sin(_alpha3) - r2 * np.cos(_gamma) - l23(flank_angle) * np.cos(flank_angle)

            return np.array(
                [
                    (
                            depth - r3 + (r3 - r2) * np.cos(_alpha3 - _alpha4) + r2 * np.sin(_gamma)
                            - _fw * np.tan(flank_angle) - l23(flank_angle) * np.sin(flank_angle)
                    ),
                    (
                            indent - (r3 + r4) * (1 - np.cos(_alpha4))
                    )
                ]
            )

        sol = root(
            f, np.array([np.pi / 4, np.pi / 4]),
        )

        if not sol.success:
            raise RuntimeError("Could not determine geometric values with given input.")

        alpha2 = sol.x[0]
        alpha3 = sol.x[1]
        alpha4 = alpha2 + alpha3 - flank_angle

    return dict(
        flank_angle=flank_angle,
        alpha2=alpha2,
        alpha3=alpha3,
        alpha4=alpha4,
    )


def solve_box_like(
        r2: float,
        r4: float,
        depth: float,
        indent: float,
        ground_width: Optional[float],
        even_ground_width: Optional[float],
        usable_width: Optional[float],
        flank_angle: Optional[float],
):
    alpha4 = np.arccos(1 - indent / (r2 + r4))

    if flank_angle is None:
        if usable_width is not None:
            if ground_width is not None:
                flank_angle = np.arctan(depth / (usable_width - ground_width) * 2)
            elif even_ground_width is not None:
                def f(_alpha):
                    _ground_width = even_ground_width + 2 * ((r4 + r2) * np.sin(alpha4) + r2 * np.tan(_alpha / 2))
                    return depth - (usable_width - _ground_width) / 2 * np.tan(_alpha)

                flank_angle = root_scalar(f, bracket=(MIN_ANGLE, MAX_ANGLE)).root
                ground_width = even_ground_width + 2 * ((r4 + r2) * np.sin(alpha4) + r2 * np.tan(flank_angle / 2))
            else:
                raise TypeError("either ground_width or even_ground_width must not be None")
        else:
            raise TypeError("usable_width must not be None if flank_angle is None")
    elif ground_width is None and even_ground_width is None:
        if usable_width is not None:
            ground_width = usable_width - 2 * depth / np.tan(flank_angle)
        else:
            raise TypeError("usable_width must not be None if ground_width and even_ground_width are None")
    elif usable_width is None:
        if ground_width is None:
            ground_width = even_ground_width + 2 * ((r4 + r2) * np.sin(alpha4) + r2 * np.tan(flank_angle / 2))

        usable_width = ground_width + 2 * depth / np.tan(flank_angle)
    else:
        raise TypeError("either flank_angle, ground_width or usable_width must be None")

    if even_ground_width is None:
        even_ground_width = ground_width - 2 * ((r4 + r2) * np.sin(alpha4) + r2 * np.tan(flank_angle / 2))

    return dict(
        ground_width=ground_width,
        usable_width=usable_width,
        flank_angle=flank_angle,
        even_ground_width=even_ground_width,
        alpha4=alpha4
    )
