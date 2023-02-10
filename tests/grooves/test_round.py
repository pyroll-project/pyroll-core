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
    g1 = RoundGroove(usable_width=31.79180677, r1=2, r2=15.8, pad_angle=0, sol_index=0)

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g1.contour_line.xy)
    plt.axline((g1.z3, g1.y3), slope=-np.tan(g1.flank_angle), c="C0", lw=1, ls="--")
    plt.axline((g1.z1, g1.y1), slope=np.tan(g1.pad_angle), c="C0", lw=1, ls="--")

    check(g1)

    g2 = RoundGroove(usable_width=31.79180677, r1=2, r2=15.8, pad_angle=0, sol_index=1)
    plt.plot(*g2.contour_line.xy)
    plt.axline((g2.z3, g2.y3), slope=-np.tan(g2.flank_angle), c="C1", lw=1, ls="--")
    plt.axline((g2.z1, g2.y1), slope=np.tan(g2.pad_angle), c="C1", lw=1, ls="--")

    plt.grid()
    plt.axhline(15.55, c="k")
    plt.ylim(-1, 18)
    plt.show()
    plt.close()


def test_round_errors():
    with pytest.raises(TypeError):
        RoundGroove(depth=15.55, usable_width=31.79180677, r1=2, r2=15.8)
    with pytest.raises(TypeError):
        RoundGroove(r1=2, r2=15.8)
