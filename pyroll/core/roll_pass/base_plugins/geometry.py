import numpy as np
from ..roll_pass import RollPass


@RollPass.tip_width
def tip_width(self):
    return self.roll.groove.usable_width + self.gap / 2 / np.tan(self.roll.groove.alpha1)


@RollPass.height
def height(self):
    return self.gap + 2 * self.roll.groove.depth


@RollPass.volume
def volume(self: RollPass):
    return (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area
            ) / 3 * self.roll.contact_length
