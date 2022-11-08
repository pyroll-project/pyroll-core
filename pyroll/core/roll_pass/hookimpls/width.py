from ..roll_pass import RollPass


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.width * self.roll_pass.spread


@RollPass.OutProfile.filling_ratio
def filling_ratio(self: RollPass.OutProfile):
    return self.width / self.roll_pass.roll.groove.usable_width
