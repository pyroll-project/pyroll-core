# this is a dummy plugin for testing purposes that is not included in the dist package
from pyroll.core import RollPass


@RollPass.roll_force
def roll_force(roll_pass: RollPass):
    return 42
