from numpy import pi, isclose

from pyroll.core.grooves import RoundGroove


def test_round():
    g = RoundGroove(depth=15.55, r1=2, r2=15.8)

    assert isclose(g.usable_width, 31.79180677)
    assert isclose(g.alpha1, 82.738129 / 180 * pi)
    assert isclose(g.alpha2, 82.738129 / 180 * pi)
    assert isclose(g.z1, 17.65722232)
