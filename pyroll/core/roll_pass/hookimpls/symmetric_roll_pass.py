import numpy as np

from ..symmetric_roll_pass import SymmetricRollPass


@SymmetricRollPass.entry_point
def entry_point(self: SymmetricRollPass):
    height_change = self.in_profile.height - self.height
    return -np.sqrt(self.roll.min_radius * height_change - height_change ** 2 / 4)


@SymmetricRollPass.velocity
def velocity(self: SymmetricRollPass):
    if self.roll.has_value("neutral_angle"):
        return self.roll.working_velocity * np.cos(self.roll.neutral_angle)
    else:
        return self.roll.working_velocity


@SymmetricRollPass.roll_force
def roll_force(self: SymmetricRollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3 * self.roll.contact_area
