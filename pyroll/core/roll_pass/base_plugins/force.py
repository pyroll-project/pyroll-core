import sys

from pyroll.core.roll_pass.roll_pass import RollPass


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    mean_flow_stress = (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3
    return mean_flow_stress * roll_pass.contact_area


@RollPass.hookimpl
def roll_torque(roll_pass: RollPass):
    return roll_pass.roll_force * roll_pass.contact_length * 0.5


RollPass.plugin_manager.register(sys.modules[__name__])
