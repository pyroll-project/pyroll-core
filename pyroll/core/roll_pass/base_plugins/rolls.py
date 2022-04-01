import sys

from ..roll_pass import RollPass


@RollPass.hookimpl
def working_roll_radius(roll_pass: RollPass):
    return roll_pass.nominal_roll_radius - roll_pass.groove.cross_section.centroid.y


@RollPass.hookimpl
def min_roll_radius(roll_pass: RollPass):
    return roll_pass.nominal_roll_radius - roll_pass.groove.depth


@RollPass.hookimpl
def max_roll_radius(roll_pass: RollPass):
    return roll_pass.nominal_roll_radius


@RollPass.hookimpl
def velocity(roll_pass: RollPass):
    if hasattr(roll_pass, "rotational_frequency"):
        return roll_pass.working_roll_radius * roll_pass.rotational_frequency


RollPass.plugin_manager.register(sys.modules[__name__])
