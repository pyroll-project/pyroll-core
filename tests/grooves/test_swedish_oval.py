import numpy as np
import pytest
from numpy import rad2deg, isclose

from pyroll.core.grooves.ovals.swedish_oval import SwedishOvalGroove


def check(g):
    assert isclose(g.even_ground_width, 16.97224362 * 2)
    assert isclose(rad2deg(g.alpha1), 33.690068)
    assert isclose(rad2deg(g.alpha2), 33.690068)
    assert isclose(g.z1, 52.4222051)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_swedish_oval_usable_width_ground_width():
    g = SwedishOvalGroove(depth=20, r1=8, r2=10, usable_width=100, ground_width=40)
    check(g)


def test_swedish_oval_usable_width_flank_angle():
    g = SwedishOvalGroove(depth=20, r1=8, r2=10, usable_width=100, flank_angle=33.690068)
    check(g)


def test_swedish_oval_ground_width_flank_angle():
    g = SwedishOvalGroove(depth=20, r1=8, r2=10, ground_width=40, flank_angle=33.690068)
    check(g)


def test_swedish_oval_all():
    with pytest.raises(TypeError):
        g = SwedishOvalGroove(
            depth=20, r1=8, r2=10, usable_width=100, ground_width=40,
            flank_angle=33.690068
            )
