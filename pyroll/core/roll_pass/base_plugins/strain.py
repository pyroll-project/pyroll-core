import logging
import sys

import numpy as np

from ..roll_pass import RollPass


@RollPass.hookimpl
def strain_change(roll_pass: RollPass):
    strain_change = np.log(roll_pass.in_profile.cross_section.area / roll_pass.out_profile.cross_section.area)

    if strain_change < 0:
        logging.getLogger(__name__).warning(
            "Negative strain change occurred. Assuming it to be zero to be able to continue iteration."
        )
        return 0

    return strain_change


@RollPass.OutProfile.hookimpl
def strain(roll_pass: RollPass):
    return roll_pass.in_profile.strain + roll_pass.strain_change


RollPass.plugin_manager.register(sys.modules[__name__])
RollPass.OutProfile.plugin_manager.register(sys.modules[__name__])
