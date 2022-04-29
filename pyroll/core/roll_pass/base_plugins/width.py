import sys

from ..roll_pass import RollPass


@RollPass.OutProfile.hookimpl
def width(roll_pass: RollPass):
    return roll_pass.in_profile.rotated.width * roll_pass.spread


RollPass.OutProfile.plugin_manager.register(sys.modules[__name__])
