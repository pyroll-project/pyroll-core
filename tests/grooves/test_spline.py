import numpy as np
from pyroll.core import SplineGroove

points = [
    (-2, 0),
    (0, 0),
    (1, 1),
    (2, 2),
    (5, 2),
    (8, 2),
    (9, 1),
    (10, 0),
    (13, 0)
]


def test_spline_with_usable_width():
    g = SplineGroove(
        points,
        usable_width=9,
        types=("oval", "swedish_oval"),
    )

    assert np.isclose(g.usable_width, 9)
    assert np.isclose(g.cross_section.area, 16)
    assert np.isclose(g.depth, 2)
    assert np.isclose(g.local_depth(1), 2)
    assert np.isclose(g.local_depth(5), 0)
    assert np.isclose(g.local_depth(4), 1)
    assert np.isclose(g.local_depth(-5), 0)
    assert np.isclose(g.local_depth(-4), 1)

    assert "oval" in g.types
    assert "swedish_oval" in g.types


def test_spline_without_usable_width():
    g = SplineGroove(
        points,
        types=("oval", "swedish_oval"),
    )

    assert np.isclose(g.usable_width, 10)
    assert np.isclose(g.cross_section.area, 16)
    assert np.isclose(g.depth, 2)
    assert np.isclose(g.local_depth(1), 2)
    assert np.isclose(g.local_depth(5), 0)
    assert np.isclose(g.local_depth(4), 1)
    assert np.isclose(g.local_depth(-5), 0)
    assert np.isclose(g.local_depth(-4), 1)

    assert "oval" in g.types
    assert "swedish_oval" in g.types
