import sys

import numpy as np
from pluggy import PluginManager

from pyroll.core.roll_pass.roll_pass import RollPass


class Specs:
    """Extra spec class to avoid name collisions with impls."""

    @staticmethod
    @RollPass.hookspec
    def cross_section_ratio(roll_pass: RollPass):
        """Calculate cross section ratio used in Hensel-Poluchin master curves."""

    @staticmethod
    @RollPass.hookspec
    def rolling_efficiency(roll_pass: RollPass):
        """Calculate rolling efficiency according to Hensel-Poluchin master curve."""

    @staticmethod
    @RollPass.hookspec
    def deformation_resistance(roll_pass: RollPass):
        """Calculate deformation resistance according to Hensel-Poluchin master curve."""

    @staticmethod
    @RollPass.hookspec
    def lever_coefficient(roll_pass: RollPass):
        """Calculate lever coefficient according to Hensel-Poluchin master curve."""


@RollPass.hookimpl
def cross_section_ratio(roll_pass: RollPass):
    mean_cross_section = (roll_pass.in_profile.cross_section + 2 * roll_pass.out_profile.cross_section) / 3
    return roll_pass.contact_area / mean_cross_section


@RollPass.hookimpl
def rolling_efficiency(roll_pass: RollPass):
    inverse_efficiency = (0.9901 + 0.106 * roll_pass.cross_section_ratio + 0.0283 * roll_pass.cross_section_ratio ** 2
                          + 1.5718 * np.exp(-2.4609 * roll_pass.cross_section_ratio)
                          + 0.3117 * np.exp(-15.625 * roll_pass.cross_section_ratio ** 2))
    return inverse_efficiency ** -1


@RollPass.hookimpl
def deformation_resistance(roll_pass: RollPass):
    return roll_pass.mean_flow_stress / roll_pass.rolling_efficiency


@RollPass.hookimpl
def lever_coefficient(roll_pass: RollPass):
    return ((np.exp(-0.6 * roll_pass.cross_section_ratio) + 0.076 * roll_pass.cross_section_ratio)
            * roll_pass.velocity ** 0.005 * np.exp(
                -0.0003 * (roll_pass.mean_temperature - 273.15 - 900)))


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    return roll_pass.deformation_resistance * roll_pass.contact_area


@RollPass.hookimpl
def roll_torque(roll_pass: RollPass):
    return roll_pass.roll_force * roll_pass.contact_length * roll_pass.lever_coefficient


RollPass.plugin_manager.add_hookspecs(Specs())
RollPass.plugin_manager.register(sys.modules[__name__])

RollPass.hooks.add("roll_force")
RollPass.hooks.add("roll_torque")
