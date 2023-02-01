import matplotlib.pyplot as plt
import numpy as np

from pyroll.core import Roll, RoundGroove


def test_line_interpolation_z():
    roll = Roll(
        groove=RoundGroove(r1=0, r2=10, depth=10),
        nominal_radius=100
    )

    interp = roll.surface_interpolation(0, roll.surface_z).squeeze()

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.plot(*roll.groove.contour_line.xy, alpha=0.5)
    ax.plot(roll.surface_z, interp, alpha=0.5)
    plt.show()
    plt.close()

    assert np.allclose(interp[1:-1], roll.groove.contour_points[:, 1])


def test_surface_plot():
    roll = Roll(
        groove=RoundGroove(r1=0, r2=10, depth=10),
        nominal_radius=100
    )

    x = np.linspace(-70, 70, 100)
    z = np.linspace(-15, 15, 50)
    interp = roll.surface_interpolation(x, z)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.invert_zaxis()
    ax.plot_surface(*np.meshgrid(roll.surface_x, roll.surface_z), roll.surface_y, alpha=0.5)
    ax.plot_surface(*np.meshgrid(x, z), interp, alpha=0.8)
    plt.show()
    plt.close()

    assert np.allclose(roll.surface_interpolation(roll.surface_x, roll.surface_z), roll.surface_y)
