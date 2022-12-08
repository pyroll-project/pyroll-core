from pathlib import Path

import jinja2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from pyroll.core import Unit, PassSequence, RollPass, Profile
from .. import utils
from ...pluggy import hookimpl, plugin_manager

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
)

_template = _env.get_template("plots.html")


@hookimpl(specname="report_unit_display")
def plots_display(unit: Unit):
    plots = [
        utils.get_svg_from_figure(p) if isinstance(p, Figure) else p
        for p in plugin_manager.hook.report_unit_plot(unit=unit)
    ]

    return _template.render(plots=plots)


@hookimpl(specname="report_unit_plot")
def roll_forces_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"roll force $F$")
        ax.set_title("Roll Forces")

        units = list(unit)
        if len(units) > 0:
            indices, forces = np.transpose(
                [
                    (index, unit.roll_force)
                    for index, unit in enumerate(units)
                    if isinstance(unit, RollPass)
                ]
            )

            ax.bar(x=indices, height=forces, width=0.8)

            return fig


@hookimpl(specname="report_unit_plot")
def roll_torques_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"roll torque $M$")
        ax.set_title("Roll Torques")

        units = list(unit)
        if len(units) > 0:
            x, y = np.transpose(
                [
                    (index, unit.roll.roll_torque)
                    for index, unit in enumerate(units)
                    if isinstance(unit, RollPass)
                ]
            )

            ax.bar(x=x, height=y, width=0.8)

            return fig


@hookimpl(specname="report_unit_plot")
def strains_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"strain $\varphi_\mathrm{V}$")
        ax.set_title("Mean Equivalent Strains")

        units = list(unit)
        if len(units) > 0:
            def gen_seq():
                yield -0.5, units[0].in_profile.strain
                for i, u in enumerate(units):
                    yield i + 0.5, u.out_profile.strain

            x, y = np.transpose(
                list(gen_seq())
            )

            ax.plot(x, y, marker="x")

            return fig


@hookimpl(specname="report_unit_plot")
def filling_ratios_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"filling ratio $i$")
        ax.set_title("Filling Ratios")

        units = list(unit)
        if len(units) > 0:
            x, y = np.transpose(
                [
                    (index, unit.out_profile.filling_ratio)
                    for index, unit in enumerate(units)
                    if isinstance(unit, RollPass)
                ]
            )

            ax.bar(x=x, height=y, width=0.8)

            return fig


@hookimpl(specname="report_unit_plot")
def cross_sections_plot(unit: Unit):
    if isinstance(unit, PassSequence):
        fig, ax = utils.create_sequence_plot(unit)
        ax.set_ylabel(r"cross section $A_\mathrm{p}$")
        ax.set_title("Profile Cross-Sections")

        units = list(unit)
        if len(units) > 0:
            def gen_seq():
                yield -0.5, units[0].in_profile.cross_section.area
                for i, u in enumerate(units):
                    yield i + 0.5, u.out_profile.cross_section.area

            x, y = np.transpose(
                list(gen_seq())
            )

            ax.plot(x, y, marker="x")

            return fig


def plot_profile(ax: plt.Axes, profile: Profile, color):
    if profile is not None:
        ax.fill(*profile.cross_section.boundary.xy, alpha=0.5, color=color)
        ax.fill(*profile.equivalent_rectangle.boundary.xy, fill=False, color=color, ls="--")


def plot_pass_groove_contour(ax: plt.Axes, roll_pass: RollPass):
    ax.plot(*roll_pass.upper_contour_line.xy, color="k")
    ax.plot(*roll_pass.lower_contour_line.xy, color="k")


@hookimpl(specname="report_unit_plot")
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
