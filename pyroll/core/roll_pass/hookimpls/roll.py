import numpy as np

from ..base import BaseRollPass
from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass


@BaseRollPass.Roll.roll_torque
def roll_torque(self: BaseRollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * 0.5


@BaseRollPass.Roll.contact_length
def contact_length(self: BaseRollPass.Roll):
    height_change = self.roll_pass.in_profile.height - self.roll_pass.height
    return np.sqrt(self.min_radius * height_change - height_change ** 2 / 4)


@BaseRollPass.Roll.contact_length
def contact_length_square_oval(self: BaseRollPass.Roll):
    if "square" in self.roll_pass.in_profile.classifiers and "oval" in self.roll_pass.classifiers:
        depth = self.groove.local_depth(self.roll_pass.in_profile.width / 2)
        height_change = self.roll_pass.in_profile.height - self.roll_pass.gap - 2 * depth
        radius = self.max_radius - depth
        return np.sqrt(radius * height_change - height_change ** 2 / 4)


@RollPass.Roll.contact_area
def contact_area(self: RollPass.Roll):
    return (self.roll_pass.in_profile.width + self.roll_pass.out_profile.width) / 2 * self.contact_length


@ThreeRollPass.Roll.contact_area
def contact_area3(self: ThreeRollPass.Roll):
    in_profile_local_width = self.roll_pass.in_profile.local_width(-self.roll_pass.in_profile.height / 2)
    return (in_profile_local_width + self.roll_pass.out_profile.contact_lines[1].width) / 2 * self.contact_length


@BaseRollPass.Roll.center
def center(self: BaseRollPass.Roll):
    return np.array([0, self.roll_pass.gap / 2 + self.nominal_radius])


@BaseRollPass.Roll.neutral_angle
def neutral_angle(self: BaseRollPass.Roll):
    if self.has_value("neutral_point"):
        return np.arcsin(self.neutral_point / self.working_radius)


@BaseRollPass.Roll.neutral_point
def neutral_point(self: BaseRollPass.Roll):
    if self.has_set_or_cached("neutral_angle"):
        return np.sin(self.neutral_angle) * self.working_radius


@BaseRollPass.Roll.surface_velocity
def surface_velocity(self: BaseRollPass.Roll):
    if self.roll_pass.has_set("velocity"):
        if self.has_value("neutral_angle"):
            return self.roll_pass.velocity / np.cos(self.neutral_angle)
        else:
            return self.roll_pass.velocity / np.cos(self.roll_pass.exit_angle)
