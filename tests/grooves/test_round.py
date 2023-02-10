import matplotlib.pyplot as plt
import numpy as np
import pytest
from numpy import isclose, rad2deg

from pyroll.core import RoundGroove


def check(g):
    assert isclose(g.depth, 15.55)
    assert isclose(g.usable_width, 31.79180677)
    assert isclose(rad2deg(g.alpha1), 82.738129)
    assert isclose(rad2deg(g.alpha2), 82.738129)
    assert isclose(g.z1, 17.65722232)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_round_usable_width():
    g = RoundGroove(depth=15.55, r1=2, r2=15.8, pad_angle=0)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.grid()
    plt.axhline(15.55, c="k")
    plt.show()
    plt.close()

    check(g)


def test_round_r2():
    g = RoundGroove(depth=15.55, usable_width=31.79180677, r1=2, pad_angle=0, r2=None)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.grid()
    plt.axhline(15.55, c="k")
    plt.show()
    plt.close()

    check(g)


def test_round_depth():
    g = RoundGroove(usable_width=31.79180677, r1=2, r2=15.8, pad_angle=0)

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.axline((g.z3, g.y3), slope=-np.tan(g.flank_angle), c="C0", lw=1, ls="--")
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="C0", lw=1, ls="--")


def test_round_errors():
    with pytest.raises(TypeError):
        RoundGroove(depth=15.55, usable_width=31.79180677, r1=2, r2=15.8)
    with pytest.raises(TypeError):
        RoundGroove(r1=2, r2=15.8)
