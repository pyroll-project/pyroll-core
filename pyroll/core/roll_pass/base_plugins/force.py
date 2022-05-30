import sys

from ...roll import Roll
from ..roll_pass import RollPass

@RollPass.hookimpl
def mean_flow_stress(roll_pass: RollPass):
    return (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    return roll_pass.mean_flow_stress * roll_pass.roll.contact_area


@RollPass.Roll.hookimpl
def roll_torque(roll_pass: RollPass, roll: Roll):
    return roll_pass.roll_force * roll.contact_length * 0.5


RollPass.plugin_manager.register(sys.modules[__name__])
RollPass.Roll.plugin_manager.register(sys.modules[__name__])
