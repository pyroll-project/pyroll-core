import numpy as np
from matplotlib import pyplot as plt
from numpy import rad2deg, isclose

from pyroll.core import FalseRoundGroove


def test_false_round():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_angle=65)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()

    assert isclose(g.usable_width, 78.13476937)
    assert isclose(rad2deg(g.alpha1), 65)
    assert isclose(rad2deg(g.alpha2), 65)
    assert isclose(g.z1, 42.2527)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_false_round3():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_angle=65, pad_angle=30)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()

    assert isclose(g.usable_width, 78.13476937)
    assert isclose(rad2deg(g.flank_angle), 65)
    assert isclose(rad2deg(g.alpha2), 65)
    assert isclose(g.z2, 39.0673769147305)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
