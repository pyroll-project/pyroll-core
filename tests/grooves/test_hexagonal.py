import numpy as np
import pytest
from numpy import rad2deg, isclose

from pyroll.core.grooves.ovals.swedish_oval import SwedishOvalGroove


def check(g):
    assert isclose(g.usable_width, 18.84529946)
    assert isclose(g.ground_width, 10)
    assert isclose(g.even_ground_width, 8.84529946)
    assert isclose(g.depth, 7.66025404)
    assert isclose(rad2deg(g.alpha1), 60)
    assert isclose(rad2deg(g.alpha2), 60)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_haxagonal_fa():
    g = SwedishOvalGroove(depth=7.66025404, r1=3, r2=1, usable_width=18.84529946, ground_width=10)
    check(g)


def test_haxagonal_gw():
    g = SwedishOvalGroove(depth=7.66025404, r1=3, r2=1, usable_width=18.84529946, flank_angle=60)
    check(g)


def test_haxagonal_uw():
    g = SwedishOvalGroove(depth=7.66025404, r1=3, r2=1, ground_width=10, flank_angle=60)
    check(g)


def test_haxagonal_fa():
    g = SwedishOvalGroove(depth=7.66025404, r1=3, r2=1, usable_width=18.84529946, even_ground_width=8.84529946)
    check(g)


def test_haxagonal_uw():
    g = SwedishOvalGroove(depth=7.66025404, r1=3, r2=1, even_ground_width=8.84529946, flank_angle=60)
    check(g)
