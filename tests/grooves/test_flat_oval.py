import numpy as np
from numpy import isclose, rad2deg

from pyroll.core import FlatOvalGroove


def check(g):
    assert isclose(g.usable_width, 60)
    assert isclose(g.even_ground_width, 9.58758548 * 2)
    assert isclose(rad2deg(g.alpha1), 78.463041)
    assert isclose(rad2deg(g.alpha2), 78.463041)
    assert isclose(g.z1, 34.0824829)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_flat_oval_uw():
    g = FlatOvalGroove(depth=20, r1=5, r2=20, usable_width=60)
    check(g)


def test_flat_oval_egw():
    g = FlatOvalGroove(depth=20, r1=5, r2=20, even_ground_width=9.58758548 * 2)
    check(g)
