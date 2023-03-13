import numpy as np

from ..roll_pass import RollPass


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * 0.5


@RollPass.Roll.contact_length
def contact_length(self: RollPass.Roll):
    height_change = self.roll_pass.in_profile.height - self.roll_pass.height
    return np.sqrt(self.min_radius * height_change - height_change ** 2 / 4)


@RollPass.Roll.contact_length
def contact_length_square_oval(self: RollPass.Roll):
    if "square" in self.roll_pass.in_profile.classifiers and "oval" in self.roll_pass.classifiers:
        depth = self.groove.local_depth(self.roll_pass.in_profile.width / 2)
        height_change = self.roll_pass.in_profile.height - self.roll_pass.gap - 2 * depth
        radius = self.max_radius - depth
        return np.sqrt(radius * height_change - height_change ** 2 / 4)


@RollPass.Roll.contact_area
def contact_area(self: RollPass.Roll):
    return (self.roll_pass.in_profile.width + self.roll_pass.out_profile.width) / 2 * self.contact_length


@RollPass.Roll.center
def center(self: RollPass.Roll):
    return np.array([0, self.roll_pass.gap / 2 + self.nominal_radius])


@RollPass.Roll.surface_velocity
def surface_velocity(self: RollPass.Roll):
    if self.roll_pass.has_set("velocity"):
        if self.has_value("neutral_point"):
            alpha = np.arcsin(-self.neutral_point / self.working_radius)
        else:
            alpha = 0
        return self.roll_pass.velocity / np.cos(alpha)
