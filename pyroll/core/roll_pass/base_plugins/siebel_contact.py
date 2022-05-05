import sys

import numpy as np
from ..roll_pass import RollPass
from ...roll import Roll


@RollPass.Roll.hookimpl
def contact_length(roll_pass: RollPass, roll: Roll):
    """
    Contact length between rolls and stock calculated using Siebel's approach
    """
    height_change = roll_pass.in_profile.height - roll_pass.height
    return np.sqrt(roll.min_radius * height_change - height_change ** 2 / 4)


@RollPass.Roll.hookimpl
def contact_area(roll_pass: RollPass, roll: Roll):
    """
    Contact area between rolls and stock calculated using Siebel's approach
    """
    return (roll_pass.in_profile.width + roll_pass.out_profile.width) / 2 * roll.contact_length


RollPass.Roll.plugin_manager.register(sys.modules[__name__])
