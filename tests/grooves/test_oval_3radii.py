import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import Oval3RadiiGroove


def test_oval3radii():
    g = Oval3RadiiGroove(depth=28.5, r1=10, r2=30, r3=170, usable_width=62.30907983 * 2)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-100, 100)
    plt.ylim(0, 30)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.z2, 62.30907983)
    assert isclose(rad2deg(g.flank_angle), 67.651448)
    assert isclose(rad2deg(g.alpha2), 54.432377)
    assert isclose(rad2deg(g.alpha3), 13.21907)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_oval3radii3():
    g = Oval3RadiiGroove(depth=28.5, r1=10, r2=30, r3=170, usable_width=62.30907983 * 2, pad_angle=30)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-100, 100)
    plt.ylim(0, 30)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.z2, 62.30907983)
    assert isclose(rad2deg(g.flank_angle), 61.962495382849674)
    assert isclose(rad2deg(g.alpha2), 49.1839949209669)
    assert isclose(rad2deg(g.alpha3), 12.778500461882771)
    assert isclose(g.z1, 71.27116358712432)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points

def test_oval3radii_r2_greater_r3():
    g = Oval3RadiiGroove(r1=7, r2=80, r3=70, usable_width=120, depth=30)

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-100, 100)
    plt.ylim(-40, 40)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.z2, 60)
    assert isclose(rad2deg(g.flank_angle), 49.4320)
    assert isclose(rad2deg(g.alpha2), 32.776)
    assert isclose(rad2deg(g.alpha3), 16.6558)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points