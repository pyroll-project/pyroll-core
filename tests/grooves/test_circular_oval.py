import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import pi, isclose, rad2deg

from pyroll.core import CircularOvalGroove


def check(g):
    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-25, 25)
    plt.ylim(0, 7)
    plt.grid()
    plt.axhline(5.05, c="k")
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    print(g.flank_angle)

    assert isclose(g.depth, 5.05)
    assert isclose(g.r2, 33)
    assert isclose(g.usable_width, 35.27599946)
    assert isclose(rad2deg(g.alpha1), 29.102618)
    assert isclose(rad2deg(g.alpha2), 29.102618)
    assert isclose(g.z1, 19.45501221)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_circular_oval_usable_width():
    g = CircularOvalGroove(depth=5.05, r1=7, r2=33)
    check(g)


def test_circular_oval_r2():
    g = CircularOvalGroove(usable_width=17.63799973 * 2, depth=5.05, r1=7)
    check(g)


def test_circular_oval_depth():
    g = CircularOvalGroove(usable_width=17.63799973 * 2, r1=7, r2=33)
    check(g)


def test_circular_oval_errors():
    with pytest.raises(TypeError):
        CircularOvalGroove(depth=5.05, usable_width=17.63799973 * 2, r1=7, r2=33)
    with pytest.raises(TypeError):
        CircularOvalGroove(r1=7, r2=33)


def check3(g):
    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-25, 25)
    plt.ylim(0, 7)
    plt.grid()
    plt.axhline(5.05, c="k")
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    print(g.flank_angle)

    assert isclose(g.depth, 5.05)
    assert isclose(g.r2, 33)
    assert isclose(g.usable_width, 35.87663862132782)
    assert isclose(g.alpha1, 0.9813435140305233)
    assert isclose(g.alpha2, 0.4577447384322245)
    assert isclose(g.z1, 21.177045876533423)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_circular_oval_usable_width3():
    g = CircularOvalGroove(depth=5.05, r1=7, r2=33, pad_angle=30)
    check3(g)


def test_circular_oval_r23():
    g = CircularOvalGroove(usable_width=35.87663862132782, depth=5.05, r1=7, pad_angle=30)
    check3(g)


def test_circular_oval_depth3():
    g = CircularOvalGroove(usable_width=35.87663862132782, r1=7, r2=33, pad_angle=30)
    check3(g)
