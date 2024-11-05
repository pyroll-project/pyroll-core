import math

import numpy as np
from shapely import Polygon, difference, clip_by_rect, MultiLineString, line_merge
from ..base import BaseRollPass
from ..three_roll_pass import ThreeRollPass
from ..roll_pass import RollPass
from ...rotator import Rotator
from ...grooves import GenericElongationGroove

from ...config import Config
from . import helpers


@BaseRollPass.rotation
def auto_rotation(self: BaseRollPass):
    return Config.ROLL_PASS_AUTO_ROTATION


@BaseRollPass.rotation
def detect_already_rotated(self: BaseRollPass):
    if Config.ROLL_PASS_AUTO_ROTATION and self.parent is not None:
        try:
            prev = self.prev
        except IndexError:
            return True

        while True:
            if isinstance(prev, BaseRollPass):
                return True
            if isinstance(prev, Rotator):
                return False
            try:
                prev = prev.prev
            except IndexError:
                return True


@BaseRollPass.orientation
def default_orientation(self: BaseRollPass):
    return 0


@BaseRollPass.roll_force
def roll_force(self: BaseRollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3 * self.roll.contact_area


@RollPass.usable_width
def usable_width(self: RollPass):
    return self.roll.groove.usable_width


@ThreeRollPass.usable_width
def usable_width3(self: BaseRollPass):
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


@ThreeRollPass.inscribed_circle_diameter
def inscribed_circle_diameter_from_gap(self: ThreeRollPass):
    if self.has_set_or_cached("gap"):
        half = self.roll.groove.usable_width / 2 / np.sqrt(3) + self.gap / np.sqrt(3) + self.roll.groove.depth
        return half * 2


@ThreeRollPass.gap
def gap3_from_height(self: ThreeRollPass):
    if self.has_set_or_cached("height"):
        return (
                self.height / 2
                - self.roll.groove.usable_width / 2 / np.sqrt(3)
                - self.roll.groove.depth
        ) * np.sqrt(3)


@ThreeRollPass.gap
def gap3_from_icd(self: ThreeRollPass):
    if self.has_set_or_cached("inscribed_circle_diameter"):
        return (
                self.inscribed_circle_diameter / 2
                - self.roll.groove.usable_width / 2 / np.sqrt(3)
                - self.roll.groove.depth
        ) * np.sqrt(3)


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
    return abs(2 * usable_contour.bounds[1])


@BaseRollPass.volume
def volume(self: BaseRollPass):
    return (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area
            ) / 3 * self.length


@BaseRollPass.surface_area
def surface_area(self: BaseRollPass):
    return (self.in_profile.cross_section.perimeter + 2 * self.out_profile.cross_section.perimeter
            ) / 3 * self.length


@RollPass.contact_area
def contact_area(self: RollPass):
    return 2 * self.roll.contact_area


@ThreeRollPass.contact_area
def contact_area3(self: ThreeRollPass):
    return 3 * self.roll.contact_area


@BaseRollPass.velocity
def velocity(self: BaseRollPass):
    if self.roll.has_value("neutral_angle"):
        return self.roll.working_velocity * np.cos(self.roll.neutral_angle)
    else:
        return self.roll.rotational_frequency * self.roll.working_radius * 2 * np.pi


@BaseRollPass.duration
def duration(self: BaseRollPass):
    return self.length / self.velocity


@BaseRollPass.length
def length(self: BaseRollPass):
    return self.roll.contact_length


@BaseRollPass.displaced_cross_section
def displaced_cross_section(self: BaseRollPass):
    return difference(self.in_profile.cross_section, self.usable_cross_section)


@BaseRollPass.reappearing_cross_section
def reappearing_cross_section(self: BaseRollPass):
    return difference(self.out_profile.cross_section, self.in_profile.cross_section)


@BaseRollPass.elongation_efficiency
def elongation_efficiency(self: BaseRollPass):
    return 1 - self.reappearing_cross_section.area / self.displaced_cross_section.area


@BaseRollPass.target_filling_ratio(trylast=True)
def default_target_filling(self: BaseRollPass):
    return 1


@BaseRollPass.target_width
def target_width_from_target_filling_ratio(self: BaseRollPass):
    if self.has_value("target_filling_ratio"):
        return self.target_filling_ratio * self.usable_width


@BaseRollPass.target_filling_ratio
def target_filling_ratio_from_target_width(self: BaseRollPass):
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


@BaseRollPass.target_cross_section_area
def target_cross_section_area_from_target_cross_section_filling_ratio(self: BaseRollPass):
    if self.has_set_or_cached("target_cross_section_filling_ratio"):
        return self.target_cross_section_filling_ratio * self.usable_cross_section.area


@BaseRollPass.target_cross_section_filling_ratio
def target_cross_section_filling_ratio_from_target_cross_section_area(self: BaseRollPass):
    if self.has_value("target_cross_section_area"):  # important has_value for computing from target_width
        return self.target_cross_section_area / self.usable_cross_section.area


@RollPass.power
def roll_power(self: RollPass):
    return 2 * self.roll.roll_power


@ThreeRollPass.power
def roll_power_3(self: ThreeRollPass):
    return 3 * self.roll.roll_power


@BaseRollPass.entry_point
def entry_point(self: BaseRollPass):
    return - self.roll.contact_length


@BaseRollPass.entry_angle
def entry_angle(self: BaseRollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        depth = self.roll.groove.local_depth(self.in_profile.width / 2)
        radius = self.roll.max_radius - depth
        return np.arcsin(self.entry_point / radius)

    return np.arcsin(self.entry_point / self.roll.min_radius)


@BaseRollPass.exit_point
def exit_point(self: BaseRollPass):
    return 0


@BaseRollPass.exit_angle
def exit_angle(self: BaseRollPass):
    return np.arcsin(self.exit_point / self.roll.working_radius)


@BaseRollPass.Profile.contact_lines
def contact_contour_lines(self: BaseRollPass.Profile):
    rp = self.roll_pass
    contact_contur_lines_possible_multilinestring = [cl.intersection(self.cross_section.exterior.buffer(1e-9)) for cl in rp.contour_lines]

    contact_contour_lines_linestring = []
    for ccl in contact_contur_lines_possible_multilinestring:
        if isinstance(ccl, MultiLineString):
            merged_ccl = line_merge(ccl)
            contact_contour_lines_linestring.append(merged_ccl)
        else:
            contact_contour_lines_linestring.append(ccl)

    return contact_contour_lines_linestring


@RollPass.front_tension
def default_front_tension(self: RollPass):
    return 0


@RollPass.back_tension
def default_back_tension(self: RollPass):
    return 0


@BaseRollPass.technologically_orientated_contour_lines
def technologically_correctly_orientated_contour_lines(self: BaseRollPass):
    return MultiLineString([self._get_oriented_geom(cl) for cl in self.contour_lines])


@BaseRollPass.OutProfile.technologically_orientated_cross_section
def technologically_correctly_orientated_cross_section(self: BaseRollPass.OutProfile):
    return self.roll_pass._get_oriented_geom(self.cross_section, orientation=self.roll_pass.orientation)

