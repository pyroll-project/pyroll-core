import numpy as np
from pyroll.core import SplineGroove
from pathlib import Path
import matplotlib.pyplot as plt

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
        classifiers=("oval", "swedish_oval"),
    )

    assert np.isclose(g.usable_width, 9)
    assert np.isclose(g.cross_section.area, 16)
    assert np.isclose(g.depth, 2)
    assert np.isclose(g.local_depth(1), 2)
    assert np.isclose(g.local_depth(5), 0)
    assert np.isclose(g.local_depth(4), 1)
    assert np.isclose(g.local_depth(-5), 0)
    assert np.isclose(g.local_depth(-4), 1)

    assert "oval" in g.classifiers
    assert "swedish_oval" in g.classifiers


def test_spline_without_usable_width():
    g = SplineGroove(
        points,
        classifiers=("oval", "swedish_oval"),
    )

    assert np.isclose(g.usable_width, 10)
    assert np.isclose(g.cross_section.area, 16)
    assert np.isclose(g.depth, 2)
    assert np.isclose(g.local_depth(1), 2)
    assert np.isclose(g.local_depth(5), 0)
    assert np.isclose(g.local_depth(4), 1)
    assert np.isclose(g.local_depth(-5), 0)
    assert np.isclose(g.local_depth(-4), 1)

    assert "oval" in g.classifiers
    assert "swedish_oval" in g.classifiers


def test_spline_from_dxf():
    script_dir = Path(__file__).resolve().parent
    dxf_file = "swedish_oval_test_groove.dxf"
    absolute_path = script_dir / dxf_file

    g = SplineGroove.from_dxf_drawing(filepath=absolute_path, classifiers=["oval", "swedish_oval"])

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()
    plt.close()

    assert np.isclose(g.usable_width, 0.0413, atol=0.001)

    assert "oval" in g.classifiers
    assert "swedish_oval" in g.classifiers
