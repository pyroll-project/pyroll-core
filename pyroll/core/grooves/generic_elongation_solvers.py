from typing import Optional

import numpy as np
from scipy.optimize import root_scalar, root, fixed_point, least_squares

# angle brackets for numerical solvers to prevent divide by zero
MIN_ANGLE = 1e-6
MAX_ANGLE = np.pi / 2 - MIN_ANGLE

__all__ = ["solve_box_like", "solve_r123", "solve_r124", "solve_r1234"]


def return_flank_height_and_width(flank_length: float, flank_width: float, flank_height: float):
    if flank_length is not None:
        def _flank_width(_alpha):
            return flank_length * np.cos(_alpha)

        def _flank_height(_alpha):
            return flank_length * np.sin(_alpha)

    elif flank_width is not None:
        def _flank_width(_alpha):
            return flank_width

        def _flank_height(_alpha):
            return flank_width * np.tan(_alpha)

    elif flank_height is not None:
        def _flank_width(_alpha):
            return flank_height / np.tan(_alpha)

        def _flank_height(_alpha):
            return flank_height

    else:
        def _flank_width(_alpha):
            return 0.0

        def _flank_height(_alpha):
            return 0.0
    return _flank_width, _flank_height


def l23(r1, pad_angle, _alpha):
    return r1 * np.tan((_alpha + pad_angle) / 2)


def solve_r123_residuals(alpha_vec, r1, r2, r3, depth, width, pad_angle, flank_width, flank_height, sign_r32):
    a2, a3 = alpha_vec
    _alpha = a2 + a3
    gamma = np.pi / 2 - _alpha
    r32 = abs(r3 - r2)
    vertical_condition = (
            depth - r3
            + sign_r32 * r32 * np.cos(a3)
            + r2 * np.sin(gamma)
            - flank_height(_alpha)
            - l23(r1, pad_angle, _alpha) * np.sin(_alpha)
    )
    horizontal_condition = (
            width / 2.0
            - sign_r32 * r32 * np.sin(a3)
            - r2 * np.cos(gamma)
            - flank_width(_alpha)
            - l23(r1, pad_angle, _alpha) * np.cos(_alpha)
    )

    return np.array([vertical_condition, horizontal_condition])


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
    if flank_angle is None:

        _flank_width, _flank_height = return_flank_height_and_width(flank_length, flank_width, flank_height)

        if width is None:

            def f(_alpha):
                return depth - r2 * (1 - np.cos(_alpha)) - l23(r1, pad_angle, _alpha) * np.sin(_alpha) - _flank_height(
                    _alpha)

            flank_angle = root_scalar(f, bracket=(MIN_ANGLE, MAX_ANGLE)).root

        elif depth is None:
            alpha4 = np.arccos(1 - indent / (r2 + r4))

            def f(_alpha):
                return (
                        width / 2
                        - r2 * np.sin(_alpha)
                        - l23(r1, pad_angle, _alpha) * np.cos(_alpha)
                        - _flank_width(_alpha)
                        - (r2 + r4) * np.sin(alpha4)
                )

            raster = np.linspace(MIN_ANGLE, MAX_ANGLE, 100)
            values = f(raster)
            lower = raster[values > 0][0]
            upper = raster[values < 0][-1]
            flank_angle = root_scalar(f, bracket=(lower, upper)).root

        elif r2 is None:

            def f(_alpha):
                _r2 = (depth - l23(r1, pad_angle, _alpha) * np.sin(_alpha) - _flank_height(_alpha)) / (
                        1 - np.cos(_alpha))
                _alpha4 = np.arccos(1 - indent / (_r2 + r4))

                return (
                        width / 2
                        - _r2 * np.sin(_alpha)
                        - l23(r1, pad_angle, _alpha) * np.cos(_alpha)
                        - _flank_width(_alpha)
                        - (_r2 + r4) * np.sin(_alpha4)
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
            depth = r2 * (1 - np.cos(flank_angle)) + (
                    width / 2 - r2 * np.sin(flank_angle) - (r2 + r4) * np.sin(alpha4)
            ) * np.tan(flank_angle)

    else:

        def f(_r2):
            _alpha4 = np.arccos(1 - indent / (_r2 + r4))
            return (depth - width / 2 * np.tan(flank_angle) + r4 * np.sin(_alpha4)) / (
                    1 - np.cos(flank_angle) - np.sin(flank_angle) * np.tan(flank_angle) - np.sin(_alpha4)
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
    _flank_width, _flank_height = return_flank_height_and_width(flank_length, flank_width, flank_height)

    if flank_angle is not None:

        def f(_alpha):
            r32 = r3 - r2
            _alpha2 = _alpha
            _alpha3 = flank_angle - _alpha
            _gamma = np.pi / 2 - flank_angle

            _fw = width / 2 - r32 * np.sin(_alpha3) - r2 * np.cos(_gamma) - l23(r1, pad_angle, flank_angle) * np.cos(
                flank_angle)

            return (
                    depth
                    - r3
                    + r32 * np.cos(_alpha3)
                    + r2 * np.sin(_gamma)
                    - _fw * np.tan(flank_angle)
                    - l23(r1, pad_angle, flank_angle) * np.sin(flank_angle)
            )

        sol = root_scalar(f, bracket=(MIN_ANGLE, MAX_ANGLE)).root
        alpha2 = sol
        alpha3 = flank_angle - sol

        return dict(
            flank_angle=flank_angle,
            alpha2=alpha2,
            alpha3=alpha3,
        )

    else:
        if r2 > r3:
            starts = [np.array([np.pi / 4, np.pi / 4]), np.array([np.pi / 6, np.pi / 3]),
                      np.array([np.pi / 3, np.pi / 6]),
                      np.array([0.2, 0.6])]

            candidates = []
            for sign in (+1.0, -1.0):
                for x0 in starts:
                    res = least_squares(
                        lambda a: solve_r123_residuals(a, r1, r2, r3, depth, width, pad_angle, _flank_width,
                                                       _flank_height, sign),
                        x0=x0,
                        bounds=([MIN_ANGLE, MIN_ANGLE], [MAX_ANGLE, MAX_ANGLE]),
                        ftol=1e-12, xtol=1e-12, gtol=1e-12, max_nfev=2000
                    )
                    if not res.success:
                        continue
                    a2, a3 = res.x
                    if a2 <= 0 or a3 <= 0:
                        continue
                    flank = a2 + a3
                    resid_norm = np.linalg.norm(res.fun)
                    candidates.append(
                        {'branch': sign, 'alpha2': float(a2), 'alpha3': float(a3), 'flank_angle': float(flank),
                         'residuum': float(resid_norm), 'start': x0})

            if not candidates:
                raise RuntimeError("No geometric feasible solution found.")

            best = min(candidates, key=lambda c: c['residuum'])

            alpha2 = best['alpha2']
            alpha3 = best['alpha3']
            flank_angle = best['flank_angle']

        else:
            r32 = r3 - r2

            def f(_alpha):
                _alpha2 = _alpha[0]
                _alpha3 = _alpha[1]
                _flank_angle = _alpha2 + _alpha3
                _gamma = np.pi / 2 - _flank_angle

                return np.array(
                    [
                        (
                                depth
                                - r3
                                + r32 * np.cos(_alpha3)
                                + r2 * np.sin(_gamma)
                                - _flank_height(_flank_angle)
                                - l23(r1, pad_angle, _flank_angle) * np.sin(_flank_angle)
                        ),
                        (
                                width / 2
                                - r32 * np.sin(_alpha3)
                                - r2 * np.cos(_gamma)
                                - _flank_width(_flank_angle)
                                - l23(r1, pad_angle, _flank_angle) * np.cos(_flank_angle)
                        ),
                    ]
                )

            sol = root(
                f,
                np.array([np.pi / 4, np.pi / 4]),
            )

            if not sol.success:
                raise RuntimeError("Could not determine geometric values with given input.")

            alpha2 = sol.x[0]
            alpha3 = sol.x[1]
            flank_angle = alpha2 + alpha3

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
    if flank_angle is None:
        _flank_height, _flank_width = return_flank_height_and_width(flank_length, flank_width, flank_height)

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
                                depth
                                - r3
                                + (r3 - r2) * np.cos(_alpha3 - _alpha4)
                                + r2 * np.sin(_gamma)
                                - _flank_height(_flank_angle)
                                - l23(r1, pad_angle, _flank_angle) * np.sin(_flank_angle)
                        ),
                        (
                                width / 2
                                - (r3 - r2) * np.sin(_alpha3 - _alpha4)
                                - r2 * np.cos(_gamma)
                                - _flank_width(_flank_angle)
                                - l23(r1, pad_angle, _flank_angle) * np.cos(_flank_angle)
                                - (r3 + r4) * np.sin(_alpha4)
                        ),
                        (indent - (r3 + r4) * (1 - np.cos(_alpha4))),
                    ]
                )
            else:
                _gamma = np.pi / 2 - _alpha4
                return np.array(
                    [
                        (
                                depth
                                - r2 * (1 - np.cos(_flank_angle))
                                - _flank_height(_flank_angle)
                                - l23(r1, pad_angle, _flank_angle) * np.sin(_flank_angle)
                        ),
                        (
                                width / 2
                                - r2 * np.sin(_flank_angle)
                                - _flank_width(_flank_angle)
                                - l23(r1, pad_angle, _flank_angle) * np.cos(_flank_angle)
                                - r4 * np.sin(_alpha4)
                                - r3 * np.cos(_gamma)
                                - (r2 - r3) * np.sin(_alpha2 - _flank_angle)
                        ),
                        (
                                indent
                                - r4 * (1 - np.cos(_alpha4))
                                + r3 * np.sin(_gamma)
                                + (r2 - r3) * np.cos(_alpha4 - _alpha3)
                                - r2
                        ),
                    ]
                )

        sol = root(
            f,
            np.array([np.pi / 4, np.pi / 4, np.pi / 4]),
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

            _fw = width / 2 - (r3 - r2) * np.sin(_alpha3) - r2 * np.cos(_gamma) - l23(r1, pad_angle,
                                                                                      flank_angle) * np.cos(flank_angle)

            return np.array(
                [
                    (
                            depth
                            - r3
                            + (r3 - r2) * np.cos(_alpha3 - _alpha4)
                            + r2 * np.sin(_gamma)
                            - _fw * np.tan(flank_angle)
                            - l23(r1, pad_angle, flank_angle) * np.sin(flank_angle)
                    ),
                    (indent - (r3 + r4) * (1 - np.cos(_alpha4))),
                ]
            )

        sol = root(
            f,
            np.array([np.pi / 4, np.pi / 4]),
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
        alpha4=alpha4,
    )
