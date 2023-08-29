import math

import numpy as np
from shapely import MultiPolygon, Polygon, difference, clip_by_rect

from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass
from ...rotator import Rotator
from ...grooves import GenericElongationGroove

from ...config import Config
from . import helpers


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
            try:
                prev = prev.prev
            except IndexError:
                return True


@RollPass.roll_force
def roll_force(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3 * self.roll.contact_area


@RollPass.usable_width
def usable_width(self: RollPass):
    return self.roll.groove.usable_width


@ThreeRollPass.usable_width
def usable_width3(self: RollPass):
    return 2 / 3 * np.sqrt(3) * (self.roll.groove.usable_width + self.gap / 2)


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


@RollPass.usable_cross_section
def usable_cross_section(self: RollPass) -> Polygon:
    return helpers.out_cross_section(self, self.usable_width)


@ThreeRollPass.usable_cross_section
def usable_cross_section3(self: ThreeRollPass) -> Polygon:
    return helpers.out_cross_section3(self, self.usable_width)


@RollPass.tip_cross_section
def tip_cross_section(self: RollPass) -> Polygon:
    return helpers.out_cross_section(self, self.tip_width)


@ThreeRollPass.tip_cross_section
def tip_cross_section3(self: ThreeRollPass) -> Polygon:
    return helpers.out_cross_section3(self, self.tip_width)


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
    usable_contour = clip_by_rect(
        self.contour_lines[1],
        -self.roll.groove.usable_width / 2,
        -math.inf,
        self.roll.groove.usable_width / 2,
        math.inf
    )
    return -2 * usable_contour.bounds[1]


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


@RollPass.displaced_cross_section
def displaced_cross_section(self: RollPass):
    return difference(self.in_profile.cross_section, self.usable_cross_section)


@RollPass.reappearing_cross_section
def reappearing_cross_section(self: RollPass):
    return difference(self.out_profile.cross_section, self.in_profile.cross_section)


@RollPass.elongation_efficiency
def elongation_efficiency(self: RollPass):
    if self.reappearing_cross_section.area == 0:
        return np.nan
    else:
        displaced_area = sum([poly.area for poly in self.displaced_cross_section.geoms])
        reappearing_area = sum([poly.area for poly in self.reappearing_cross_section.geoms])
        return 1 - reappearing_area / displaced_area


@RollPass.target_filling_ratio(trylast=True)
def default_target_filling(self: RollPass):
    return 1


@RollPass.target_width
def target_width_from_target_filling_ratio(self: RollPass):
    if self.has_value("target_filling_ratio"):
        return self.target_filling_ratio * self.usable_width


@RollPass.target_filling_ratio
def target_filling_ratio_from_target_width(self: RollPass):
    if self.has_set_or_cached("target_width"):
        return self.target_width / self.usable_width


@RollPass.target_cross_section_area
def target_cross_section_area_from_target_width(self: RollPass):
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section(self, self.target_width)
        return target_cross_section.area


@ThreeRollPass.target_cross_section_area
def target_cross_section_area_from_target_width3(self: ThreeRollPass):
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section3(self, self.target_width)
        return target_cross_section.area


@RollPass.target_cross_section_area
def target_cross_section_area_from_target_cross_section_filling_ratio(self: RollPass):
    if self.has_set_or_cached("target_cross_section_filling_ratio"):
        return self.target_cross_section_filling_ratio * self.usable_cross_section.area


@RollPass.target_cross_section_filling_ratio
def target_cross_section_filling_ratio_from_target_cross_section_area(self: RollPass):
    if self.has_value("target_cross_section_area"):  # important has_value for computing from target_width
        return self.target_cross_section_area / self.usable_cross_section.area


@RollPass.power
def roll_power(self: RollPass):
    return 2 * self.roll.roll_power


@ThreeRollPass.power
def roll_power_3(self: ThreeRollPass):
    return 3 * self.roll.roll_power
