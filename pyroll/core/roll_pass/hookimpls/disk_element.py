import numpy as np
from ..base import BaseRollPass


@BaseRollPass.DiskElement.length
def length(self: BaseRollPass.DiskElement):
    return self.roll_pass.roll.contact_length / self.roll_pass.disk_element_count


@BaseRollPass.DiskElement.velocity
def disk_velocity(self: BaseRollPass.DiskElement):
    return self.roll_pass.velocity


@BaseRollPass.DiskElement.duration
def disk_duration(self: BaseRollPass.DiskElement):
    return self.length / self.velocity


@BaseRollPass.DiskElement.Profile.longitudinal_angle
def longitudinal_angle(self: BaseRollPass.DiskElement.Profile):
    return np.arcsin(self.x / self.roll_pass.roll.working_radius)
