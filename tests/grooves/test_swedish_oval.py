import pytest
from numpy import pi, isclose

from pyroll.core.grooves import SwedishOvalGroove


def test_swedish_oval_usable_width_ground_width():
    g = SwedishOvalGroove(depth=20, r1=8, r2=10, usable_width=100, ground_width=40)

    assert isclose(g.even_ground_width, 16.97224362 * 2)
    assert isclose(g.alpha1, 33.690068 / 180 * pi)
    assert isclose(g.alpha2, 33.690068 / 180 * pi)
    assert isclose(g.z1, 52.4222051)


def test_swedish_oval_usable_width_flank_angle():
    g = SwedishOvalGroove(depth=20, r1=8, r2=10, usable_width=100, flank_angle=33.690068 / 180 * pi)

    assert isclose(g.even_ground_width, 16.97224362 * 2)
    assert isclose(g.alpha1, 33.690068 / 180 * pi)
    assert isclose(g.alpha2, 33.690068 / 180 * pi)
    assert isclose(g.z1, 52.4222051)


def test_swedish_oval_ground_width_flank_angle():
    g = SwedishOvalGroove(depth=20, r1=8, r2=10, ground_width=40, flank_angle=33.690068 / 180 * pi)

    assert isclose(g.even_ground_width, 16.97224362 * 2)
    assert isclose(g.alpha1, 33.690068 / 180 * pi)
    assert isclose(g.alpha2, 33.690068 / 180 * pi)
    assert isclose(g.z1, 52.4222051)


def test_swedish_oval_all():
    with pytest.raises(ValueError):
        g = SwedishOvalGroove(depth=20, r1=8, r2=10, usable_width=100, ground_width=40, flank_angle=33.690068 / 180 * pi)
