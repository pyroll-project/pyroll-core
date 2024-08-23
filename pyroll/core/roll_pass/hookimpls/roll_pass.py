import numpy as np
from shapely import Polygon

from . import helpers
from ..roll_pass import RollPass
from ...grooves import GenericElongationGroove


@RollPass.usable_width
def usable_width(self: RollPass):
    return self.roll.groove.usable_width


@RollPass.tip_width
def tip_width(self):
    if isinstance(self.roll.groove, GenericElongationGroove):
        return self.roll.groove.usable_width + self.gap / 2 / np.tan(self.roll.groove.flank_angle)


@RollPass.usable_cross_section
def usable_cross_section(self: RollPass) -> Polygon:
    return helpers.out_cross_section(self, self.usable_width)


@RollPass.tip_cross_section
def tip_cross_section(self: RollPass) -> Polygon:
    return helpers.out_cross_section(self, self.tip_width)


@RollPass.gap
def gap(self: RollPass):
    if self.has_set_or_cached("height"):
        return self.height - 2 * self.roll.groove.depth


@RollPass.height
def height(self):
    if self.has_set_or_cached("gap"):
        return self.gap + 2 * self.roll.groove.depth


@RollPass.contact_area
def contact_area(self: RollPass):
    return 2 * self.roll.contact_area


@RollPass.target_cross_section_area
def target_cross_section_area_from_target_width(self: RollPass):
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section(self, self.target_width)
        return target_cross_section.area


@RollPass.power
def roll_power(self: RollPass):
    return 2 * self.roll.roll_power


@RollPass.entry_point
def entry_point(self: RollPass):
    height_change = self.in_profile.height - self.height
    return np.sqrt(self.roll.min_radius * height_change - height_change ** 2 / 4)


@RollPass.entry_point
def entry_point_square_oval(self: RollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        depth = self.roll.groove.local_depth(self.in_profile.width / 2)
        height_change = self.in_profile.height - self.gap - 2 * depth
        radius = self.roll.max_radius - depth
        return np.sqrt(radius * height_change - height_change ** 2 / 4)


@RollPass.velocity
def velocity(self: RollPass):
    if self.roll.has_value("neutral_angle"):
        return self.roll.working_velocity * np.cos(self.roll.neutral_angle)
    else:
        return self.roll.working_velocity


@RollPass.roll_force
def roll_force(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3 * self.roll.contact_area
