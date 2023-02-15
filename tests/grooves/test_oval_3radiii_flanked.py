import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose, rad2deg

from pyroll.core import Oval3RadiiFlankedGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-90, 90)
    plt.ylim(0, 45)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.z1, 78.715)
    assert isclose(rad2deg(g.alpha1), 73.3028)
    assert isclose(rad2deg(g.alpha2), 56.34657)
    assert isclose(rad2deg(g.alpha3), 16.95623)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_oval3radii_flanked_fa():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_angle=90 - 16.697244
    )
    check(g)


def test_oval3radii_flanked_fh():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_height=13.141969810727078
    )
    check(g)


def test_oval3radii_flanked_fw():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_width=3.9420908619510726
    )
    check(g)


def test_oval3radii_flanked_fl():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_length=13.720475606550236
    )
    check(g)


def check3(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.xlim(-90, 90)
    plt.ylim(0, 45)
    plt.axline((g.z3, g.y3), slope=np.tan(-g.flank_angle), c="r", ls="--", lw=1)
    plt.axline((g.z1, g.y1), slope=np.tan(g.pad_angle), c="r", ls="--", lw=1)
    plt.show()
    plt.close()

    assert isclose(g.z1, 80.81865289177068)
    assert isclose(rad2deg(g.alpha1), 103.30275599999999)
    assert isclose(rad2deg(g.alpha2), 56.34657)
    assert isclose(rad2deg(g.alpha3), 16.95623)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_oval3radii_flanked_fa3():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_angle=90 - 16.697244, pad_angle=30
    )
    check3(g)


def test_oval3radii_flanked_fh3():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_height=10.153779034948355, pad_angle=30
    )
    check3(g)


def test_oval3radii_flanked_fw3():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_width=3.0457473365422203, pad_angle=30
    )
    check3(g)


def test_oval3radii_flanked_fl3():
    g = Oval3RadiiFlankedGroove(
        depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
        flank_length=10.600745517585581, pad_angle=30
    )
    check3(g)
