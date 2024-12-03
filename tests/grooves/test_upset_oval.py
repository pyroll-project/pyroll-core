import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import UpsetOvalGroove


def test_upset_oval():
    g = UpsetOvalGroove(depth=23.3303, r1=3, r2=30, r3=5, usable_width=26.2495)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-15, 15)
    plt.ylim(0, 45)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(rad2deg(g.flank_angle), 84.78409143)
    assert isclose(rad2deg(g.alpha2), 41.94044839)
    assert isclose(rad2deg(g.alpha3), 85.68728609 / 2)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
