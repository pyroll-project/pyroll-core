import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import SquareGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()

    assert isclose(rad2deg(g.flank_angle), 44.5)
    assert isclose(rad2deg(g.alpha2), 44.5)
    assert isclose(g.z2, 15)
    assert isclose(g.depth, 13.53436275)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_square_usable_width_tip_depth():
    g = SquareGroove(r1=5, r2=3, usable_width=30, tip_depth=14.74045895)
    check(g)


def test_square_usable_width_tip_angle():
    g = SquareGroove(r1=5, r2=3, usable_width=30, tip_angle=91)
    check(g)


def test_square_tip_depth_tip_angle():
    g = SquareGroove(r1=5, r2=3, tip_depth=14.74045895, tip_angle=91)
    check(g)


def test_square_all():
    with pytest.raises(ValueError):
        SquareGroove(r1=5, r2=3, usable_width=30, tip_depth=14.74045895, tip_angle=91)


def test_square_large_tip_angle():
    with pytest.raises(ValueError):
        SquareGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=120)


def test_square_small_tip_angle():
    with pytest.raises(ValueError):
        SquareGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=60)


def test_square_usable_width_tip_depth3():
    g = SquareGroove(r1=5, r2=3, usable_width=30, tip_depth=14.74045895, pad_angle=30)
    check(g)


def test_square_usable_width_tip_angle3():
    g = SquareGroove(r1=5, r2=3, usable_width=30, tip_angle=91, pad_angle=30)
    check(g)


def test_square_tip_depth_tip_angle3():
    g = SquareGroove(r1=5, r2=3, tip_depth=14.74045895, tip_angle=91, pad_angle=30)
    check(g)
