import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import DiamondGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()

    assert isclose(rad2deg(g.flank_angle), 30)
    assert isclose(rad2deg(g.alpha2), 30)
    assert isclose(g.z2, 20)
    assert isclose(g.depth, 10.30940108)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_diamond_usable_width_tip_depth():
    g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_depth=11.54700538)
    check(g)


def test_diamond_usable_width_tip_angle():
    g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_angle=120)
    check(g)


def test_diamond_tip_depth_tip_angle():
    g = DiamondGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=120)
    check(g)


def test_diamond_all():
    with pytest.raises(ValueError):
        DiamondGroove(r1=5, r2=8, usable_width=40, tip_depth=11.54700538, tip_angle=120)


def test_diamond_usable_width_tip_depth3():
    g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_depth=11.54700538, pad_angle=30)
    check(g)


def test_diamond_usable_width_tip_angle3():
    g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_angle=120, pad_angle=30)
    check(g)


def test_diamond_tip_depth_tip_angle3():
    g = DiamondGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=120, pad_angle=30)
    check(g)
