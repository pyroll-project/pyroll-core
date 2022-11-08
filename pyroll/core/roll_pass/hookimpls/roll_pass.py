import numpy as np

from ..roll_pass import RollPass


@RollPass.label
def label(self: RollPass):
    return "RollPass"


@RollPass.mean_flow_stress
def mean_flow_stress(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3


@RollPass.roll_force
def roll_force(self: RollPass):
    return self.mean_flow_stress * self.roll.contact_area


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


@RollPass.velocity
def velocity(self: RollPass):
    return self.roll.working_radius * self.roll.rotational_frequency


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


@RollPass.strain_rate
def strain_rate(self: RollPass):
    return self.velocity / self.roll.contact_length * self.draught
