import numpy as np
import pytest
from numpy import pi, isclose

from pyroll.core import SquareGroove


def test_square_usable_width_tip_depth():
    g = SquareGroove(r1=5, r2=3, usable_width=30, tip_depth=14.74045895)

    assert isclose(g.alpha1, 44.5 / 180 * pi)
    assert isclose(g.alpha2, 44.5 / 180 * pi)
    assert isclose(g.z1, 17.04555401)
    assert isclose(g.depth, 13.53436275)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_square_usable_width_tip_angle():
    g = SquareGroove(r1=5, r2=3, usable_width=30, tip_angle=91 / 180 * pi)

    assert isclose(g.alpha1, 44.5 / 180 * pi)
    assert isclose(g.alpha2, 44.5 / 180 * pi)
    assert isclose(g.z1, 17.04555401)
    assert isclose(g.depth, 13.53436275)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_square_tip_depth_tip_angle():
    g = SquareGroove(r1=5, r2=3, tip_depth=14.74045895, tip_angle=91 / 180 * pi)

    assert isclose(g.usable_width, 30)
    assert isclose(g.alpha1, 44.5 / 180 * pi)
    assert isclose(g.alpha2, 44.5 / 180 * pi)
    assert isclose(g.z1, 17.04555401)
    assert isclose(g.depth, 13.53436275)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_square_tip_depth_tip_angle():
    with pytest.raises(ValueError):
        g = SquareGroove(r1=5, r2=3, usable_width=30, tip_depth=14.74045895, tip_angle=91 / 180 * pi)


def test_square_large_tip_angle():
    with pytest.raises(ValueError):
        SquareGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=120 / 180 * pi)


def test_square_small_tip_angle():
    with pytest.raises(ValueError):
        SquareGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=60 / 180 * pi)
