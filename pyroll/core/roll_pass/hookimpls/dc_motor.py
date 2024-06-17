import numpy as np

from ..roll_pass import RollPass


@RollPass.DCMotor.frictional_torque
def frictional_torque(self: RollPass.DCMotor):
    if self.roll_pass.roll.has_set("neck_radius"):
        return self.roll_pass.roll_force * 2 * self.roll_pass.roll.neck_radius * self.bearing_friction_coefficient
    else:
        return self.roll_pass.roll.torque * 2 * (1 + self.bearing_friction_coefficient)


@RollPass.DCMotor.static_torque
def static_torque(self: RollPass.DCMotor):
    return self.roll_pass.torque + self.frictional_torque + self.roll_pass.idle_torque


@RollPass.DCMotor.rotational_frequency
def rotational_frequency(self: RollPass.DCMotor):
    return self.roll_pass.roll.rotation_frequency / self.gear_ratio
