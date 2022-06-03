import sys
import numpy as np
from ..roll_pass import RollPass


@RollPass.hookimpl
def tip_width(roll_pass):
    return roll_pass.roll.groove.usable_width + roll_pass.gap / 2 / np.tan(roll_pass.roll.groove.alpha1)


@RollPass.hookimpl
def height(roll_pass):
    return roll_pass.gap + 2 * roll_pass.roll.groove.depth


@RollPass.hookimpl
def volume(roll_pass: RollPass):
    return (roll_pass.in_profile.cross_section.area + 2 * roll_pass.out_profile.cross_section.area
            ) / 3 * roll_pass.roll.contact_length


RollPass.plugin_manager.register(sys.modules[__name__])
