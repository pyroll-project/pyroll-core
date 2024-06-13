import numpy as np
from ..roll_pass import RollPass


@RollPass.DiskElement.length
def length(self: RollPass.DiskElement):
    return self.roll_pass.roll.contact_length / self.roll_pass.disk_element_count


@RollPass.DiskElement.velocity
def disk_velocity(self: RollPass.DiskElement):
    return self.roll_pass.velocity


@RollPass.DiskElement.duration
def disk_duration(self: RollPass.DiskElement):
    return self.length / self.velocity


@RollPass.DiskElement.Profile.roll_angle
def roll_angle(self: RollPass.DiskElement.InProfile):
    return np.arcsin(self.x / self.roll_pass.roll.working_radius)
