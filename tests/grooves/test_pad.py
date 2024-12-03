import matplotlib.pyplot as plt

from pyroll.core import BoxGroove


def test_generic_two_roll():
    g = BoxGroove(r1=2, r2=2, depth=10, usable_width=20, ground_width=10, pad_angle=0)

    assert g.y1 == g.y2
    assert g.z12 == g.z1

    assert g.z0 > g.z1
    assert g.y0 == g.y1

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_points.T)
    plt.show()


def test_generic_three_roll():
    g = BoxGroove(r1=2, r2=2, depth=10, usable_width=20, ground_width=10, pad_angle=30)

    assert g.y1 > g.y2
    assert g.z12 < g.z1

    assert g.z0 > g.z1
    assert g.y0 > g.y1

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_points.T)
    plt.show()


def test_generic_four_roll():
    g = BoxGroove(r1=2, r2=2, depth=10, usable_width=20, ground_width=10, pad_angle=45)

    assert g.y1 > g.y2
    assert g.z12 < g.z1

    assert g.z0 > g.z1
    assert g.y0 > g.y1

    plt.figure(dpi=300)
    plt.axes().set_aspect("equal")
    plt.plot(*g.contour_points.T)
    plt.show()
