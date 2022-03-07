import sys

from ..roll_pass import RollPass, RollPassOutProfile


@RollPassOutProfile.hookimpl
def width(roll_pass: RollPass):
    return roll_pass.in_profile.rotated.width + roll_pass.width_change


RollPassOutProfile.plugin_manager.register(sys.modules[__name__])
