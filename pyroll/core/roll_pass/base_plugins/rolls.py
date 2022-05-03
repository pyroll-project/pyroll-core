import sys

from ..roll_pass import RollPass


@RollPass.hookimpl
def velocity(roll_pass: RollPass):
    if hasattr(roll_pass.roll, "rotational_frequency"):
        return roll_pass.roll.working_radius * roll_pass.roll.rotational_frequency


RollPass.plugin_manager.register(sys.modules[__name__])
