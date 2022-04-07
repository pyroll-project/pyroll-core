import sys
import numpy as np

from ..roll_pass import RollPass


@RollPass.hookimpl
def tip_width(roll_pass):
    return roll_pass.groove.usable_width + roll_pass.gap / 2 / np.tan(roll_pass.groove.alpha1)


@RollPass.hookimpl
def height(roll_pass):
    return roll_pass.gap + 2 * roll_pass.groove.depth


RollPass.plugin_manager.register(sys.modules[__name__])
