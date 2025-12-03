from ..base import BaseRollPass
from ..two_roll_pass import TwoRollPass
from ..three_roll_pass import ThreeRollPass


@TwoRollPass.Engine.torque
def engine_torque(self: TwoRollPass.Engine):
    return 2 * self.roll_pass.roll.roll_torque / (self.spindle_efficiency * self.gear_box_efficiency) + self.idle_torque


@ThreeRollPass.Engine.torque
def engine_torque(self: ThreeRollPass.Engine):
    return 3 * self.roll_pass.roll.roll_torque / (self.spindle_efficiency * self.gear_box_efficiency) + self.idle_torque


@BaseRollPass.Engine.rotational_frequency
def engine_rotational_frequency(self: BaseRollPass.Engine):
    if self.has_set_or_cached("gear_ratio"):
        return self.roll_pass.roll.rotational_frequency * self.gear_ratio
    else:
        return self.roll_pass.roll.rotational_frequency

@BaseRollPass.Engine.available_power
def available_power(self: BaseRollPass.Engine):
    if self.has_set_or_cached("base_rotational_frequency"):
        return self.maximum_power * (self.rotational_frequency / self.base_rotational_frequency)
    else:
        return self.maximum_power