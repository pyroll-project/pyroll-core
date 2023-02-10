import numpy as np
from matplotlib import pyplot as plt
from numpy import rad2deg, isclose

from pyroll.core import FalseRoundGroove

FW = 3.2814933761920244
FH = 7.037185254850074
FL = np.sqrt(FW ** 2 + FH ** 2)


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()

    assert isclose(g.depth, 31.8646)
    assert isclose(g.usable_width, 78.13476937)
    assert isclose(rad2deg(g.flank_angle), 65)
    assert isclose(rad2deg(g.alpha2), 65)
    assert isclose(g.z2, 39.0673769147305)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_false_round_usable_width_fa():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_angle=65)
    check(g)


def test_false_round_depth_fa():
    g = FalseRoundGroove(usable_width=78.13476937, r1=5, r2=38, flank_angle=65)
    check(g)


def test_false_round_r2_fa():
    g = FalseRoundGroove(depth=31.8646, usable_width=78.13476937, r1=5, flank_angle=65)
    check(g)


def test_false_round_usable_width_fw():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_width=FW)
    check(g)


def test_false_round_depth_fw():
    g = FalseRoundGroove(usable_width=78.13476937, r1=5, r2=38, flank_width=FW)
    check(g)


def test_false_round_r2_fw():
    g = FalseRoundGroove(depth=31.8646, usable_width=78.13476937, r1=5, flank_width=FW)
    check(g)


def test_false_round_usable_width_fh():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_height=FH)
    check(g)


def test_false_round_depth_fh():
    g = FalseRoundGroove(usable_width=78.13476937, r1=5, r2=38, flank_height=FH)
    check(g)


def test_false_round_r2_fh():
    g = FalseRoundGroove(depth=31.8646, usable_width=78.13476937, r1=5, flank_height=FH)
    check(g)


def test_false_round_usable_width_fl():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_length=FL)
    check(g)


def test_false_round_depth_fl():
    g = FalseRoundGroove(usable_width=78.13476937, r1=5, r2=38, flank_length=FL)
    check(g)


def test_false_round_r2_fl():
    g = FalseRoundGroove(depth=31.8646, usable_width=78.13476937, r1=5, flank_length=FL)
    check(g)


def test_false_round3():
    g = FalseRoundGroove(depth=31.8646, r1=5, r2=38, flank_angle=65, pad_angle=30)
    check(g)
