import numpy as np
from numpy import pi, isclose

from pyroll.core import Oval3RadiiGroove


def test_oval3radii():
    g = Oval3RadiiGroove(depth=28.5, r1=10, r2=30, r3=170, usable_width=62.30907983 * 2)

    assert isclose(g.z1, 69.01)
    assert isclose(g.alpha1, 67.651448 / 180 * pi)
    assert isclose(g.alpha2, 54.432377 / 180 * pi)
    assert isclose(g.alpha3, 13.21907 / 180 * pi)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
