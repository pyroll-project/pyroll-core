import numpy as np
from numpy import pi, isclose

from pyroll.core import ConstrictedSwedishOvalGroove


def check(g):
    assert isclose(g.even_ground_width, 14.81966011 * 2)
    assert isclose(g.alpha1, 63.434949 / 180 * pi)
    assert isclose(g.alpha2, 100.304846 / 180 * pi)
    assert isclose(g.alpha4, 36.869898 / 180 * pi)
    assert isclose(g.z1, 42.09016994)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_constricted_swedish_oval_usable_width_ground_width():
    g = ConstrictedSwedishOvalGroove(depth=18, r1=5, r2=10, r4=5, usable_width=39 * 2, ground_width=30 * 2, indent=3)
    check(g)


def test_constricted_swedish_oval_usable_width_flank_angle():
    g = ConstrictedSwedishOvalGroove(depth=18, r1=5, r2=10, r4=5, usable_width=39 * 2, flank_angle=63.434949 / 180 * pi,
                                     indent=3)
    check(g)


def test_constricted_swedish_oval_ground_width_flank_angle():
    g = ConstrictedSwedishOvalGroove(depth=18, r1=5, r2=10, r4=5, ground_width=30 * 2, flank_angle=63.434949 / 180 * pi,
                                     indent=3)
    check(g)
