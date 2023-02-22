import matplotlib.pyplot as plt
import numpy as np
import pytest

from pyroll.core import Roll, RoundGroove, ConstrictedBoxGroove, Oval3RadiiFlankedGroove


def test_line_interpolation_z():
    roll = Roll(
        groove=RoundGroove(r1=2, r2=10, depth=10),
        nominal_radius=100
    )

    interp = roll.surface_interpolation(0, roll.surface_z).squeeze()

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.plot(*roll.groove.contour_line.xy, alpha=0.5)
    ax.plot(roll.surface_z, interp, alpha=0.5)
    plt.show()
    plt.close()

    assert np.allclose(interp, roll.groove.contour_points[:, 1])


@pytest.mark.parametrize(
    "g",
    [
        RoundGroove(r1=2, r2=10, depth=10),
        ConstrictedBoxGroove(r1=5, r2=10, r4=5, usable_width=100, flank_angle=85, depth=20, indent=5),
        Oval3RadiiFlankedGroove(depth=41.1, r1=6, r2=23.5, r3=183, usable_width=74.2506498 * 2,
                                flank_angle=(90 - 16.697244))
    ]
)
def test_surface_plot(g):
    roll = Roll(
        groove=g,
        nominal_radius=200,
        contact_length=50,
    )
    x = np.linspace(-100, 100, 100)
    z = np.linspace(-g.z1 * 1.1, g.z1 * 1.1, 50)
    interp = roll.surface_interpolation(x, z)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, dpi=600)
    ax.invert_zaxis()
    ax.plot_surface(*np.meshgrid(roll.surface_x, roll.surface_z), roll.surface_y, alpha=0.5)
    ax.plot_surface(*np.meshgrid(x, z), interp, alpha=0.8)
    plt.show()
    plt.close()

    assert np.allclose(roll.surface_interpolation(roll.surface_x, roll.surface_z), roll.surface_y)
