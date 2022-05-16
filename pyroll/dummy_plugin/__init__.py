# this is a dummy plugin for testing purposes that is not included in the dist package
import sys

from pyroll.core import RollPass


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    return 42


RollPass.plugin_manager.register(sys.modules[__name__])
