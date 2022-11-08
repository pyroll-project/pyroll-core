import numpy as np

from ..roll_pass import RollPass


@RollPass.InProfile.x
def entry_point(self: RollPass.InProfile):
    return -self.roll_pass.roll.contact_length


@RollPass.OutProfile.x
def exit_point(self: RollPass.OutProfile):
    return 0


@RollPass.OutProfile.strain
def strain(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.strain + self.roll_pass.log_elongation


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    return self.roll_pass.roll.groove.usable_width


@RollPass.OutProfile.filling_ratio
def filling_ratio(self: RollPass.OutProfile):
    return self.width / self.roll_pass.roll.groove.usable_width
