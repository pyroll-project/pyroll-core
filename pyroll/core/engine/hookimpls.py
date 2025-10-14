import numpy as np

from .engine import Engine
from ..transport import Transport

@Engine.gear_box_efficiency
def gear_box_efficiency_becker(self: Engine):
    return 0.95

@Engine.spindle_efficiency
def spindle_efficiency_becker(self: Engine):
    return 0.98

@Engine.idle_torque
def default_idle_torque(self: Engine):
    return 0

@Engine.power
def roll_power(self: Engine):
    return self.torque * self.rotational_frequency * 2 * np.pi

@Engine.mean_power
def mean_power(self: Engine):
    try:
        next_transport = self.roll_pass.next_of(Transport)
    except (IndexError, ValueError):
        return np.sqrt(self.torque ** 2 * self.roll_pass.duration / self.roll_pass.duration)

    return np.sqrt(self.torque ** 2 * self.roll_pass.duration / (next_transport.duration + self.roll_pass.duration))