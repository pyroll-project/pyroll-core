from numpy import pi, isclose

from pyroll.core.grooves import ConstrictedBoxGroove


def check(g):
    assert isclose(g.even_ground_width, 43.5252396 * 2)
    assert isclose(g.alpha1, 75.101163 / 180 * pi)
    assert isclose(g.alpha2, 125.095962 / 180 * pi)
    assert isclose(g.alpha4, 49.994799 / 180 * pi)
    assert isclose(g.z1, 104.17595817)


def test_constricted_box_usable_width_ground_width():
    g = ConstrictedBoxGroove(depth=52, r1=15, r2=18, r4=10, usable_width=185.29, ground_width=157.62, indent=10)
    check(g)


def test_constricted_box_usable_width_flank_angle():
    g = ConstrictedBoxGroove(depth=52, r1=15, r2=18, r4=10, usable_width=185.29, flank_angle=75.101163 / 180 * pi,
                             indent=10)
    check(g)


def test_constricted_box_ground_width_flank_angle():
    g = ConstrictedBoxGroove(depth=52, r1=15, r2=18, r4=10, ground_width=157.62, flank_angle=75.101163 / 180 * pi,
                             indent=10)
    check(g)
