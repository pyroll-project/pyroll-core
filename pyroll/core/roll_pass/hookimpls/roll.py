import numpy as np

from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass
from ...config import GROOVE_PADDING


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * 0.5


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


@ThreeRollPass.Roll.contour_points
def contour_points(self: ThreeRollPass.Roll):
    """With flanks of 120°"""
    points = np.zeros((len(self.groove.contour_points) + 2, 2), dtype=float)
    points[1:-1] = self.groove.contour_points
    pad = self.groove.width * GROOVE_PADDING
    z_max = 0.5 * self.groove.width + pad
    points[0, 0] = -z_max
    points[-1, 0] = z_max

    y = pad * np.tan(np.pi / 6)
    points[0, 1] = y
    points[-1, 1] = y

    return points
