import matplotlib.pyplot as plt
import numpy as np
import pytest
from numpy import isclose, rad2deg

from pyroll.core import RoundGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-100, 100)
    plt.ylim(0, 30)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.depth, 15.55)
    assert isclose(g.usable_width, 31.79180677)
    assert isclose(rad2deg(g.alpha1), 82.738129)
    assert isclose(rad2deg(g.alpha2), 82.738129)
    assert isclose(g.z1, 17.65722232)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_round_usable_width():
    g = RoundGroove(depth=15.55, r1=2, r2=15.8, pad_angle=0)
    check(g)


def test_round_r2():
    g = RoundGroove(depth=15.55, usable_width=31.79180677, r1=2, pad_angle=0, r2=None)
    check(g)


def test_round_depth():
    g = RoundGroove(usable_width=31.79180677, r1=2, r2=15.8, pad_angle=0)
    check(g)


def test_round_errors():
    with pytest.raises(TypeError):
        RoundGroove(depth=15.55, usable_width=31.79180677, r1=2, r2=15.8)
    with pytest.raises(TypeError):
        RoundGroove(r1=2, r2=15.8)


def check3(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-25, 25)
    plt.ylim(0, 17)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.depth, 15.55)
    assert isclose(g.usable_width, 32.09051094172619)
    assert isclose(rad2deg(g.alpha1), 109.03747996761948)
    assert isclose(rad2deg(g.alpha2), 79.03747996761949)
    assert isclose(g.z1, 18.475181877968073)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_round_usable_width3():
    g = RoundGroove(depth=15.55, r1=2, r2=15.8, pad_angle=30)
    check3(g)


def test_round_r23():
    g = RoundGroove(depth=15.55, usable_width=32.09051094172619, r1=2, pad_angle=30)
    check3(g)


def test_round_depth3():
    g = RoundGroove(usable_width=32.09051094172619, r1=2, r2=15.8, pad_angle=30)
    check3(g)