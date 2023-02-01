import numpy as np
from numpy import pi, isclose

from pyroll.core import FlatOvalGroove


def test_flat_oval():
    g = FlatOvalGroove(depth=20, r1=5, r2=20, usable_width=60)

    assert isclose(g.even_ground_width, 9.58758548 * 2)
    assert isclose(g.alpha1, 78.463041 / 180 * pi)
    assert isclose(g.alpha2, 78.463041 / 180 * pi)
    assert isclose(g.z1, 34.0824829)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
