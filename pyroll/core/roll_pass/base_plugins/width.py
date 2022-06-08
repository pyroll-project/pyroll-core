import sys

from ..roll_pass import RollPass


@RollPass.OutProfile.hookimpl
def width(roll_pass: RollPass):
    return roll_pass.in_profile.width * roll_pass.spread


@RollPass.OutProfile.hookimpl
def filling_ratio(roll_pass: RollPass, profile: RollPass.OutProfile):
    return profile.width / roll_pass.roll.groove.usable_width


RollPass.OutProfile.plugin_manager.register(sys.modules[__name__])
