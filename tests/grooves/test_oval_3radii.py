import numpy as np
from numpy import isclose, rad2deg

from pyroll.core import Oval3RadiiGroove


def test_oval3radii():
    g = Oval3RadiiGroove(depth=28.5, r1=10, r2=30, r3=170, usable_width=62.30907983 * 2)

    assert isclose(g.z1, 69.01)
    assert isclose(rad2deg(g.alpha1), 67.651448)
    assert isclose(rad2deg(g.alpha2), 54.432377)
    assert isclose(rad2deg(g.alpha3), 13.21907)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
