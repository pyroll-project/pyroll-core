import sys
from matplotlib import pyplot as plt

from pyroll.core import RollPass, Profile
from ..reporter import Reporter


def plot_profile(ax: plt.Axes, profile: Profile, color):
    if profile is not None:
        ax.fill(*profile.cross_section.boundary.xy, alpha=0.5, color=color)
        ax.fill(*profile.equivalent_rectangle.boundary.xy, fill=False, color=color, ls="--")


def plot_pass_groove_contour(ax: plt.Axes, roll_pass: RollPass):
    ax.plot(*roll_pass.upper_contour_line.xy, color="k")
    ax.plot(*roll_pass.lower_contour_line.xy, color="k")


@Reporter.hookimpl
def unit_plot(unit):
    """Plot roll pass contour and its profiles"""

    if isinstance(unit, RollPass):
        fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
        ax: plt.Axes = fig.subplots()

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        plot_pass_groove_contour(ax, unit)
        plot_profile(ax, unit.in_profile, "red")
        plot_profile(ax, unit.out_profile, "blue")

        return fig


Reporter.plugin_manager.register(sys.modules[__name__])
