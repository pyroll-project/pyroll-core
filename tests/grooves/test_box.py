import numpy as np
import pytest
from numpy import pi, isclose

from pyroll.core.grooves import BoxGroove


def test_box_usable_width_ground_width():
    g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, ground_width=157.62)

    assert isclose(g.even_ground_width, 64.97285019 * 2)
    assert isclose(g.alpha1, 75.101163 / 180 * pi)
    assert isclose(g.alpha2, 75.101163 / 180 * pi)
    assert isclose(g.z1, 104.1759581)


def test_box_usable_width_flank_angle():
    g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, flank_angle=75.101163 / 180 * pi)

    assert isclose(g.even_ground_width, 64.97285019 * 2)
    assert isclose(g.alpha1, 75.101163 / 180 * pi)
    assert isclose(g.alpha2, 75.101163 / 180 * pi)
    assert isclose(g.z1, 104.1759581)


def test_box_ground_width_flank_angle():
    g = BoxGroove(depth=52, r1=15, r2=18, ground_width=157.62, flank_angle=75.101163 / 180 * pi)

    assert isclose(g.even_ground_width, 64.97285019 * 2)
    assert isclose(g.alpha1, 75.101163 / 180 * pi)
    assert isclose(g.alpha2, 75.101163 / 180 * pi)
    assert isclose(g.z1, 104.1759581)


def test_box_ground_all():
    with pytest.raises(ValueError):
        g = BoxGroove(depth=52, r1=15, r2=18, usable_width=185.29, ground_width=157.62,
                      flank_angle=75.101163 / 180 * pi)
