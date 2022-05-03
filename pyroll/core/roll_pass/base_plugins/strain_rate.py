import sys

from ..roll_pass import RollPass


@RollPass.hookimpl
def strain_rate(roll_pass: RollPass):
    return roll_pass.velocity / roll_pass.roll.contact_length * roll_pass.strain_change


RollPass.plugin_manager.register(sys.modules[__name__])
