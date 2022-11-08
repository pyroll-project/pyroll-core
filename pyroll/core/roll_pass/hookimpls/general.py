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
    if hasattr(self.roll, "rotational_frequency"):
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


@RollPass.strain_change
def strain_change(self: RollPass):
    strain_change = np.log(self.in_profile.cross_section.area / self.out_profile.cross_section.area)

    if strain_change < 0:
        logging.getLogger("RollPass").warning(
            "Negative strain change occurred. Assuming it to be zero to be able to continue iteration."
        )
        return 0

    return strain_change


@RollPass.OutProfile.equivalent_strain
def strain(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.equivalent_strain + self.roll_pass.strain_change


@RollPass.strain_rate
def strain_rate(self: RollPass):
    return self.velocity / self.roll.contact_length * self.strain_change


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.width * self.roll_pass.spread


@RollPass.OutProfile.filling_ratio
def filling_ratio(self: RollPass.OutProfile):
    return self.width / self.roll_pass.roll.groove.usable_width
