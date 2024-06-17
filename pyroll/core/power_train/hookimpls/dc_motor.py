import numpy as np

from pyroll.core.power_train.dc_motor import DCMotor


@DCMotor.torque
def torque(self: DCMotor):
    if self.has_value("dynamic_torque"):
        return self.static_torque + self.dynamic_torque
    else:
        return self.static_torque


@DCMotor.power
def power(self: DCMotor):
    return self.torque * self.rotational_frequency * 2 * np.pi


@DCMotor.bearing_friction_coefficient
def bearing_friction_coefficient(self: DCMotor):
    return 0.002


@DCMotor.bearing_efficiency
def bearing_efficiency(self: DCMotor):
    return 0.99


@DCMotor.gearbox_efficiency
def gearbox_efficiency(self: DCMotor):
    return 0.95
