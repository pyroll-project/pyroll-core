import sys
from typing import Sequence

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.transforms import Affine2D

from pyroll import RollPass, Profile
from pyroll.utils.hookutils import applies_to_unit_types
from ..report import Report


def plot_profile(ax: plt.Axes, profile: Profile, rotation_angle: float = 0, **kwargs):
    z_max = profile.width / 2
    transform = Affine2D().rotate_deg(rotation_angle) + ax.transData
    z_values = np.linspace(-z_max, z_max, 100)
    y_values = profile.groove.contour_line(z_values)
    ax.fill_between(z_values, -y_values - profile.gap / 2, y_values + profile.gap / 2, alpha=0.5, transform=transform,
                    **kwargs)


def plot_pass_groove_contour(ax: plt.Axes, roll_pass: RollPass, **kwargs):
    z_max = 1.1 * roll_pass.groove.usable_width / 2
    z_values = np.linspace(-z_max, z_max, 100)
    y_values = roll_pass.groove.contour_line(z_values)
    ax.plot(z_values, y_values + roll_pass.gap / 2, **kwargs)
    ax.plot(z_values, -y_values - roll_pass.gap / 2, **kwargs)


@Report.hookimpl
@applies_to_unit_types(RollPass)
def unit_plot(unit: RollPass):
    """Plot the temperatures of all units"""
    fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)

    plot_pass_groove_contour(ax, unit, color="black")
    if unit.in_profile is not None:
        plot_profile(ax, unit.in_profile, color="red", rotation_angle=unit.in_profile.rotation)
    if unit.out_profile is not None:
        plot_profile(ax, unit.out_profile, color="blue")

    return fig


Report.plugin_manager.register(sys.modules[__name__])
