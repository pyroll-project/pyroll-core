import numpy as np

from ..roll_pass import RollPass
from ...rotator import Rotator
from ...grooves import GenericElongationGroove

from ...config import ROLL_PASS_AUTO_ROTATION


@RollPass.rotation
def auto_rotation(self: RollPass):
    return ROLL_PASS_AUTO_ROTATION


@RollPass.rotation
def detect_already_rotated(self: RollPass):
    if ROLL_PASS_AUTO_ROTATION and self.parent is not None:
        prev = self.prev
        while True:
            if isinstance(prev, RollPass):
                return True
            if isinstance(prev, Rotator):
                return False
            prev = prev.prev


@RollPass.roll_force
def roll_force(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3 * self.contact_area / 2


@RollPass.tip_width
def tip_width(self):
    if isinstance(self.roll.groove, GenericElongationGroove):
        return self.roll.groove.usable_width + self.gap / 2 / np.tan(self.roll.groove.alpha1)


@RollPass.height
def height(self):
    return self.gap + 2 * self.roll.groove.depth


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


@RollPass.velocity
def velocity(self: RollPass):
    return self.roll.working_radius * self.roll.rotational_frequency


@RollPass.duration
def duration(self: RollPass):
    return self.length / self.velocity


@RollPass.length
def length(self: RollPass):
    return self.roll.contact_length
