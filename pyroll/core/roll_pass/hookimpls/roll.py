import numpy as np

from ..roll_pass import RollPass


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return self.roll_pass().roll_force * self.contact_length * 0.5


@RollPass.Roll.contact_length
def contact_length(self: RollPass.Roll):
    """
    Contact length between rolls and stock calculated using Siebel's approach
    """
    height_change = self.roll_pass().in_profile.height - self.roll_pass().height
    return np.sqrt(self.min_radius * height_change - height_change ** 2 / 4)


@RollPass.Roll.contact_area
def contact_area(self: RollPass.Roll):
    """
    Contact area between rolls and stock calculated using Siebel's approach
    """
    return (self.roll_pass().in_profile.width + self.roll_pass().out_profile.width) / 2 * self.contact_length


@RollPass.Roll.center
def center(self: RollPass.Roll):
    return np.array([0, self.roll_pass().gap / 2 + self.nominal_radius])
