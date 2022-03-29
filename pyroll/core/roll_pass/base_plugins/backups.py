import sys

from ..roll_pass import RollPass


@RollPass.hookimpl
def gap(roll_pass):
    return 0


@RollPass.hookimpl
def velocity(roll_pass):
    return 1


RollPass.plugin_manager.register(sys.modules[__name__])
