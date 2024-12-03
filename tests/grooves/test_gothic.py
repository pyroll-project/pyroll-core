import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import GothicGroove


def test_gothic():
    g = GothicGroove(depth=20, r1=3, r2=40, r3=2, usable_width=40)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-25, 25)
    plt.ylim(0, 25)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(rad2deg(g.flank_angle), 63.53145034330032)
    assert isclose(rad2deg(g.alpha2), 37.570020102675095)
    assert isclose(rad2deg(g.alpha3), 25.961430240625226)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
