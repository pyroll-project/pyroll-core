import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import ConstrictedCircularOvalGroove


def test_circular_oval():
    g = ConstrictedCircularOvalGroove(depth=17, r1=3, r2=30, r3=5, r4=20, indent=3, usable_width=56.70672071)

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-33, 33)
    plt.ylim(0, 18)
    plt.grid()
    plt.axhline(17, c="k")
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.depth, 17)
    assert isclose(g.usable_width, 56.70672071)
    assert isclose(rad2deg(g.alpha1), 66.80015682)
    assert isclose(rad2deg(g.alpha2), 38.44252024)
    assert isclose(rad2deg(g.alpha3), 56.71527315)
    assert isclose(rad2deg(g.alpha4), 56.71527315 / 2)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_circular_oval_egw():
    g = ConstrictedCircularOvalGroove(
        depth=17, r1=3, r2=30, r3=5, r4=20, indent=3, usable_width=56.70672071 + 5, even_ground_width=5
    )

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-35, 35)
    plt.ylim(0, 18)
    plt.grid()
    plt.axhline(17, c="k")
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.depth, 17)
    assert isclose(g.usable_width, 56.70672071 + 5)
    assert isclose(rad2deg(g.alpha1), 66.80015682)
    assert isclose(rad2deg(g.alpha2), 38.44252024)
    assert isclose(rad2deg(g.alpha3), 56.71527315)
    assert isclose(rad2deg(g.alpha4), 56.71527315 / 2)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_circular_oval_small_r2():
    g = ConstrictedCircularOvalGroove(depth=16, r1=5, r2=30, r3=5, r4=10, indent=10, usable_width=46.67222164 * 2)

    plt.figure(dpi=600)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-50, 50)
    plt.ylim(0, 18)
    plt.grid()
    plt.axhline(16, c="k")
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.depth, 16)
    assert isclose(g.usable_width, 46.67222164 * 2)
    assert isclose(rad2deg(g.alpha1), 57.12165044)
    assert isclose(rad2deg(g.alpha2), 71.37168313)
    assert isclose(rad2deg(g.alpha3), 53.13010235)
    assert isclose(rad2deg(g.alpha4), 67.38013505)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points
