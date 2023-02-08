import numpy as np
import pytest
from numpy import pi, isclose, rad2deg

from pyroll.core import DiamondGroove


def check(g):
    assert isclose(rad2deg(g.alpha1), 30)
    assert isclose(rad2deg(g.alpha2), 30)
    assert isclose(g.z1, 21.33974596)
    assert isclose(g.depth, 10.30940108)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_diamond_usable_width_tip_depth():
    g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_depth=11.54700538)
    check(g)

def test_diamond_usable_width_tip_angle():
    g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_angle=120)
    check(g)


def test_diamond_tip_depth_tip_angle():
    g = DiamondGroove(r1=5, r2=8, tip_depth=11.54700538, tip_angle=120)
    check(g)


def test_diamond_all():
    with pytest.raises(ValueError):
        g = DiamondGroove(r1=5, r2=8, usable_width=40, tip_depth=11.54700538, tip_angle=120)
