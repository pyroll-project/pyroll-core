import sys

import numpy as np

from ..roll_pass import RollPass


@RollPass.hookimpl
def contact_length(roll_pass: RollPass):
    height_change = roll_pass.in_profile.rotated.height - roll_pass.height
    return np.sqrt(roll_pass.min_roll_radius * height_change - height_change ** 2 / 4)


@RollPass.hookimpl
def contact_area(roll_pass: RollPass):
    return (roll_pass.in_profile.rotated.width + roll_pass.out_profile.width) / 2 * roll_pass.contact_length


RollPass.plugin_manager.register(sys.modules[__name__])
