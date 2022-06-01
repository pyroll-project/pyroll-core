import sys

from ..roll_pass import RollPass


@RollPass.OutProfile.hookimpl
def width(roll_pass: RollPass):
    eq_out_width = roll_pass.in_profile.equivalent_rectangle.width * roll_pass.spread
    diff = eq_out_width - roll_pass.out_profile.equivalent_rectangle.width

    return roll_pass.out_profile.width + diff


@RollPass.OutProfile.hookimpl
def filling_ratio(roll_pass: RollPass, profile: RollPass.OutProfile):
    return profile.width / roll_pass.roll.groove.usable_width


RollPass.OutProfile.plugin_manager.register(sys.modules[__name__])
