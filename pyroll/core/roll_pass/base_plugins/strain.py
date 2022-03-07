import sys

import numpy as np

from ..roll_pass import RollPass, RollPassOutProfile


@RollPass.hookimpl
def strain_change(roll_pass: RollPass):
    strain = np.log(roll_pass.in_profile.cross_section / roll_pass.out_profile.cross_section)
    return strain


@RollPassOutProfile.hookimpl
def strain(roll_pass: RollPass):
    return roll_pass.in_profile.strain + roll_pass.strain_change


RollPass.plugin_manager.register(sys.modules[__name__])
RollPassOutProfile.plugin_manager.register(sys.modules[__name__])
