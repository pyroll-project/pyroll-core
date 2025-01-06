import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import ConstrictedUpsetBoxGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_points.T)
    plt.show()

    assert isclose(g.ground_width, 9.42038116)
    assert isclose(g.usable_width, 20)
    assert isclose(g.even_ground_width, 0.51280002)
    assert isclose(rad2deg(g.flank_angle), 80)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_constricted_upset_box_fa():
    g = ConstrictedUpsetBoxGroove(depth=30, r1=5, r2=3, usable_width=20, ground_width=9.42038116, indent=0.5, r4=1)
    check(g)


def test_constricted_upset_box_gw():
    g = ConstrictedUpsetBoxGroove(depth=30, r1=5, r2=3, usable_width=20, flank_angle=80, indent=0.5, r4=1)
    check(g)


def test_constricted_upset_box_uw():
    g = ConstrictedUpsetBoxGroove(depth=30, r1=5, r2=3, flank_angle=80, ground_width=9.42038116, indent=0.5, r4=1)
    check(g)


def test_constricted_upset_box_fa_even():
    g = ConstrictedUpsetBoxGroove(depth=30, r1=5, r2=3, usable_width=20, indent=0.5, r4=1, even_ground_width=0.51280002)
    check(g)


def test_constricted_upset_box_uw_even():
    g = ConstrictedUpsetBoxGroove(depth=30, r1=5, r2=3, flank_angle=80, indent=0.5, r4=1, even_ground_width=0.51280002)
    check(g)
