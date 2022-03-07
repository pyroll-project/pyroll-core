import sys

from ..roll_pass import RollPass


@RollPass.hookimpl
def mean_temperature(roll_pass: RollPass):
    return (roll_pass.in_profile.temperature + roll_pass.out_profile.temperature) / 2


@RollPass.hookimpl
def mean_flow_stress(roll_pass: RollPass):
    return (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3


RollPass.plugin_manager.register(sys.modules[__name__])
