import numpy as np
from matplotlib import pyplot as plt
from numpy import isclose

from pyroll.core import EquivalentRibbedGroove


def check(g):
    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_points.T)
    plt.show()

    assert isclose(g.r1, 0.2)
    assert isclose(g.r3, 3.45)
    assert isclose(g.usable_width, 13.6788)
    assert isclose(g.depth, 5.5091)

    assert isclose(g.r2, 24.0753)

    assert not np.any(np.isclose(np.diff(g.contour_points[:, 0]), 0))  # test for duplicated points


def test_equivalent_ribbed_groove_r2():
    g = EquivalentRibbedGroove(
        r1=0.2,
        r3=3.45,
        rib_distance=8.4,
        rib_width=1.6,
        rib_angle=45,
        base_body_height=11.78,
        nominal_outer_diameter=14,
        usable_width=13.6788,
        depth=5.5091,
    )
    check(g)
