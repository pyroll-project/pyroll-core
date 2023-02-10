import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import pi, isclose, rad2deg

from pyroll.core import CircularOvalGroove


def check(g):
    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.grid()
    plt.axhline(5.05, c="k")
    plt.show()
    plt.close()

    assert isclose(g.depth, 5.05)
    assert isclose(g.r2, 33)
    assert isclose(g.usable_width, 17.63799973 * 2)
    assert isclose(rad2deg(g.alpha1), 29.102618)
    assert isclose(rad2deg(g.alpha2), 29.102618)
    assert isclose(g.z1, 19.45501221)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_circular_oval_depth():
    g = CircularOvalGroove(depth=5.05, r1=7, r2=33)
    check(g)


def test_circular_oval_r2():
    g = CircularOvalGroove(usable_width=17.63799973 * 2, depth=5.05, r1=7)
    check(g)


def test_circular_oval_usable_width():
    g = CircularOvalGroove(usable_width=17.63799973 * 2, r1=7, r2=33)
    check(g)


def test_circular_oval_errors():
    with pytest.raises(TypeError):
        CircularOvalGroove(depth=5.05, usable_width=17.63799973 * 2, r1=7, r2=33)
    with pytest.raises(TypeError):
        CircularOvalGroove(r1=7, r2=33)
