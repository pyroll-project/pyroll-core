import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose
from pyroll.core import FlatGroove


def test_flat():
    g = FlatGroove(usable_width=100)

    assert isclose(g.usable_width, 100)
    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_flat_3fold():
    g = FlatGroove(usable_width=100, pad_angle=30, r1=20)

    assert isclose(g.usable_width, 100)
    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points

    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_line.xy)
    plt.show()
