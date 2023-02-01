import numpy as np
from numpy import pi, isclose

from pyroll.core import Oval3RadiiFlankedGroove


def test_oval3radii_flanked():
    g = Oval3RadiiFlankedGroove(depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
                                flank_angle=(90 - 16.697244) / 180 * pi)

    assert isclose(g.z1, 78.715)
    assert isclose(g.alpha1, 73.3028 / 180 * pi)
    assert isclose(g.alpha2, 56.34657 / 180 * pi)
    assert isclose(g.alpha3, 16.95623 / 180 * pi)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
