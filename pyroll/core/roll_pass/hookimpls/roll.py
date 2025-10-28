import numpy as np

from ..two_roll_pass import TwoRollPass
from ..three_roll_pass import ThreeRollPass
from ..symmetric_roll_pass import SymmetricRollPass
from ..asymmetric_two_roll_pass import AsymmetricTwoRollPass


@SymmetricRollPass.Roll.roll_torque
def roll_torque(self: SymmetricRollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * 0.5


@SymmetricRollPass.Roll.contact_length
def contact_length(self: SymmetricRollPass.Roll):
    return self.roll_pass.exit_point - self.roll_pass.entry_point


@SymmetricRollPass.Roll.contact_area
def contact_area(self: TwoRollPass.Roll):
    return (self.roll_pass.in_profile.width + self.roll_pass.out_profile.width) / 2 * self.contact_length


@ThreeRollPass.Roll.contact_area
def contact_area3(self: ThreeRollPass.Roll):
    in_profile_local_width = self.roll_pass.in_profile.local_width(-self.roll_pass.in_profile.height / 2)
    return (in_profile_local_width + self.roll_pass.out_profile.contact_lines.geoms[1].width) / 2 * self.contact_length


@SymmetricRollPass.Roll.center
def center(self: SymmetricRollPass.Roll):
    return np.array([0, self.roll_pass.gap / 2 + self.nominal_radius])


@SymmetricRollPass.Roll.neutral_angle
def neutral_angle(self: SymmetricRollPass.Roll):
    if self.has_value("neutral_point"):
        return np.arcsin(self.neutral_point / self.working_radius)


@SymmetricRollPass.Roll.neutral_point
def neutral_point(self: SymmetricRollPass.Roll):
    if self.has_set_or_cached("neutral_angle"):
        return np.sin(self.neutral_angle) * self.working_radius


@SymmetricRollPass.Roll.working_velocity
def working_velocity(self: SymmetricRollPass.Roll):
    if self.roll_pass.has_set("velocity"):
        if self.has_value("neutral_angle"):
            return self.roll_pass.velocity / np.cos(self.neutral_angle)
        else:
            return self.roll_pass.velocity / np.cos(self.exit_angle)


@SymmetricRollPass.Roll.rotational_frequency
def rotational_frequency_from_engine(self: SymmetricRollPass.Roll, cycle):
    if not cycle:
        if self.roll_pass.engine.has_set_or_cached("gear_ratio") and self.roll_pass.engine.has_set_or_cached(
                "rotational_frequency"):
            return self.roll_pass.engine.rotational_frequency / self.roll_pass.engine.gear_ratio


@SymmetricRollPass.Roll.entry_angle
def entry_angle(self: SymmetricRollPass.Roll):
    return np.arcsin(self.roll_pass.entry_point / self.working_radius)


@SymmetricRollPass.Roll.exit_angle
def exit_angle(self: SymmetricRollPass.Roll):
    return np.arcsin(self.roll_pass.exit_point / self.working_radius)


@SymmetricRollPass.Roll.contact_duration
def contact_duration(self: SymmetricRollPass.Roll):
    return self.contact_length / self.roll_pass.velocity


@SymmetricRollPass.Roll.idle_duration
def idle_duration(self: SymmetricRollPass.Roll):
    return 1 / self.rotational_frequency - self.contact_duration


@AsymmetricTwoRollPass.UpperRoll.contact_length
def contact_length(self: AsymmetricTwoRollPass.UpperRoll):
    return self.roll_pass.exit_point - self.roll_pass.entry_point


@AsymmetricTwoRollPass.LowerRoll.contact_length
def contact_length(self: AsymmetricTwoRollPass.LowerRoll):
    return self.roll_pass.exit_point - self.roll_pass.entry_point


@AsymmetricTwoRollPass.UpperRoll.contact_area
def contact_area_asymmetric(self: AsymmetricTwoRollPass.UpperRoll):
    return (self.roll_pass.in_profile.width + self.roll_pass.out_profile.width) / 2 * self.contact_length


@AsymmetricTwoRollPass.LowerRoll.contact_area
def contact_area_asymmetric(self: AsymmetricTwoRollPass.LowerRoll):
    return (self.roll_pass.in_profile.width + self.roll_pass.out_profile.width) / 2 * self.contact_length


@AsymmetricTwoRollPass.UpperRoll.roll_torque
def roll_torque(self: AsymmetricTwoRollPass.UpperRoll):
    return self.roll_pass.roll_force * self.contact_length * 0.5


@AsymmetricTwoRollPass.LowerRoll.roll_torque
def roll_torque(self: AsymmetricTwoRollPass.LowerRoll):
    return self.roll_pass.roll_force * self.contact_length * 0.5