import numpy as np

from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass
from ...rotator import Rotator
from ...grooves import GenericElongationGroove

from ...config import Config


@RollPass.rotation
def auto_rotation(self: RollPass):
    return Config.ROLL_PASS_AUTO_ROTATION


@RollPass.rotation
def detect_already_rotated(self: RollPass):
    if Config.ROLL_PASS_AUTO_ROTATION and self.parent is not None:
        try:
            prev = self.prev
        except IndexError:
            return True

        while True:
            if isinstance(prev, RollPass):
                return True
            if isinstance(prev, Rotator):
                return False
            prev = prev.prev


@RollPass.roll_force
def roll_force(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3 * self.roll.contact_area


@RollPass.tip_width
def tip_width(self):
    if isinstance(self.roll.groove, GenericElongationGroove):
        return self.roll.groove.usable_width + self.gap / 2 / np.tan(self.roll.groove.flank_angle)


@ThreeRollPass.tip_width
def tip_width3(self):
    if isinstance(self.roll.groove, GenericElongationGroove):
        return (
                2 / 3 * np.sqrt(3) * (self.roll.groove.usable_width + self.gap / 2)
                + self.gap / np.sqrt(3) * np.cos(self.roll.groove.flank_angle)
        )


@RollPass.gap
def gap(self: RollPass):
    if self.has_set_or_cached("height"):
        return self.height - 2 * self.roll.groove.depth


@RollPass.height
def height(self):
    if self.has_set_or_cached("gap"):
        return self.gap + 2 * self.roll.groove.depth


@ThreeRollPass.height
def height3(self):
    return -2 * self.contour_lines[1].bounds[1]


@RollPass.volume
def volume(self: RollPass):
    return (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area
            ) / 3 * self.length


@RollPass.surface_area
def surface_area(self: RollPass):
    return (self.in_profile.cross_section.perimeter + 2 * self.out_profile.cross_section.perimeter
            ) / 3 * self.length


@RollPass.contact_area
def contact_area(self: RollPass):
    return 2 * self.roll.contact_area


@ThreeRollPass.contact_area
def contact_area3(self: ThreeRollPass):
    return 3 * self.roll.contact_area


@RollPass.velocity
def velocity(self: RollPass):
    if self.roll.has_value("neutral_point"):
        alpha = np.arcsin(-self.roll.neutral_point / self.roll.working_radius)
    else:
        alpha = 0
    return self.roll.surface_velocity * np.cos(alpha)


@RollPass.duration
def duration(self: RollPass):
    return self.length / self.velocity


@RollPass.length
def length(self: RollPass):
    return self.roll.contact_length
