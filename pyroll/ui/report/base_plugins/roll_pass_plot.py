import sys
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from shapely.affinity import rotate

from pyroll import RollPass, Profile
from pyroll.utils.hookutils import applies_to_unit_types
from ..report import Report


def plot_profile(ax: plt.Axes, profile: Profile, color):
    if profile is not None:
        ax.fill(*rotate(profile.cross_section, angle=profile.rotation, origin=(0, 0)).boundary.xy, alpha=0.5,
                color=color)
        ax.add_artist(
            Rectangle(
                (-profile.equivalent_rectangle.width / 2, - profile.equivalent_rectangle.height / 2),
                profile.equivalent_rectangle.width, profile.equivalent_rectangle.height,
                fill=False, color=color, ls="--"
            )
        )


def plot_pass_groove_contour(ax: plt.Axes, roll_pass: RollPass):
    ax.plot(*roll_pass.upper_contour_line.xy, color="k")
    ax.plot(*roll_pass.lower_contour_line.xy, color="k")


@Report.hookimpl
@applies_to_unit_types(RollPass)
def unit_plot(unit: RollPass):
    """Plot roll pass contour and its profiles"""
    fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
    ax: plt.Axes = fig.subplots()

    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)

    plot_pass_groove_contour(ax, unit)
    plot_profile(ax, unit.in_profile, "red")
    plot_profile(ax, unit.out_profile, "blue")

    return fig


Report.plugin_manager.register(sys.modules[__name__])
