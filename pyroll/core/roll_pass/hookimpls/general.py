import logging

import numpy as np

from ..roll_pass import RollPass


@RollPass.mean_flow_stress
def mean_flow_stress(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3


@RollPass.roll_force
def roll_force(self: RollPass):
    return self.mean_flow_stress * self.roll.contact_area


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * 0.5


@RollPass.tip_width
def tip_width(self):
    return self.roll.groove.usable_width + self.gap / 2 / np.tan(self.roll.groove.alpha1)


@RollPass.height
def height(self):
    return self.gap + 2 * self.roll.groove.depth


@RollPass.volume
def volume(self: RollPass):
    return (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area
            ) / 3 * self.roll.contact_length


@RollPass.InProfile.x
def entry_point(self: RollPass.InProfile):
    return -self.roll_pass.roll.contact_length


@RollPass.OutProfile.x
def exit_point(self: RollPass.OutProfile):
    return 0


@RollPass.velocity
def velocity(self: RollPass):
    return self.roll.working_radius * self.roll.rotational_frequency


@RollPass.Roll.contact_length
def contact_length(self: RollPass.Roll):
    """
    Contact length between rolls and stock calculated using Siebel's approach
    """
    height_change = self.roll_pass.in_profile.height - self.roll_pass.height
    return np.sqrt(self.min_radius * height_change - height_change ** 2 / 4)


@RollPass.Roll.contact_area
def contact_area(self: RollPass.Roll):
    """
    Contact area between rolls and stock calculated using Siebel's approach
    """
    return (self.roll_pass.in_profile.width + self.roll_pass.out_profile.width) / 2 * self.contact_length


@RollPass.Roll.center
def center(self: RollPass.Roll):
    return np.array([0, self.roll_pass.gap / 2 + self.nominal_radius])


@RollPass.draught
def draught(self: RollPass):
    return self.in_profile.equivalent_rectangle.height / self.out_profile.equivalent_rectangle.height


@RollPass.spread
def spread(self: RollPass):
    return self.in_profile.equivalent_rectangle.height / self.out_profile.equivalent_rectangle.height


@RollPass.elongation
def elongation(self: RollPass):
    return self.in_profile.cross_section.area / self.out_profile.cross_section.area


@RollPass.log_draught
def log_draught(self: RollPass):
    return np.log(self.draught)


@RollPass.log_spread
def log_spread(self: RollPass):
    return np.log(self.spread)


@RollPass.log_elongation
def log_elongation(self: RollPass):
    return np.log(self.elongation)


@RollPass.OutProfile.strain
def strain(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.strain + self.roll_pass.log_elongation


@RollPass.strain_rate
def strain_rate(self: RollPass):
    return self.velocity / self.roll.contact_length * self.draught


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    return self.roll_pass.roll.groove.usable_width


@RollPass.OutProfile.filling_ratio
def filling_ratio(self: RollPass.OutProfile):
    return self.width / self.roll_pass.roll.groove.usable_width
