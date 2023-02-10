import numpy as np
import pytest
from matplotlib import pyplot as plt
from numpy import pi, isclose, rad2deg

from pyroll.core import BoxGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_points.T)
    plt.show()

    assert isclose(g.even_ground_width, 64.97285019 * 2)
    assert isclose(rad2deg(g.flank_angle), 75.101163)
    assert isclose(g.z2, 92.645)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_box_usable_width_ground_width():
    g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, ground_width=157.62)
    check(g)


def test_box_usable_width_flank_angle():
    g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, flank_angle=75.101163)
    check(g)


def test_box_ground_width_flank_angle():
    g = BoxGroove(depth=52, r1=15, r2=18, ground_width=157.62, flank_angle=75.101163)
    check(g)


def test_box_ground_all():
    with pytest.raises(ValueError):
        g = BoxGroove(
            depth=52, r1=15, r2=18, usable_width=185.29, ground_width=157.62,
            flank_angle=75.101163
        )


def test_box_usable_width_ground_width3():
    g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, ground_width=157.62, pad_angle=30)
    check(g)


def test_box_usable_width_flank_angle3():
    g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, flank_angle=75.101163, pad_angle=30)
    check(g)


def test_box_ground_width_flank_angle3():
    g = BoxGroove(depth=52, r1=15, r2=18, ground_width=157.62, flank_angle=75.101163, pad_angle=30)
    check(g)
