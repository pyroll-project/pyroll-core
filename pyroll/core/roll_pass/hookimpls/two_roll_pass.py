import numpy as np
from shapely import Polygon

from . import helpers
from ..two_roll_pass import TwoRollPass
from ...grooves import GenericElongationGroove


@TwoRollPass.usable_width
def usable_width(self: TwoRollPass):
    return self.roll.groove.usable_width


@TwoRollPass.tip_width
def tip_width(self):
    if isinstance(self.roll.groove, GenericElongationGroove):
        return self.roll.groove.usable_width + self.gap / 2 / np.tan(self.roll.groove.flank_angle)


@TwoRollPass.usable_cross_section
def usable_cross_section(self: TwoRollPass) -> Polygon:
    return helpers.out_cross_section(self, self.usable_width)


@TwoRollPass.tip_cross_section
def tip_cross_section(self: TwoRollPass) -> Polygon:
    return helpers.out_cross_section(self, self.tip_width)


@TwoRollPass.gap
def gap(self: TwoRollPass):
    if self.has_set_or_cached("height"):
        return self.height - 2 * self.roll.groove.depth


@TwoRollPass.height
def height(self):
    if self.has_set_or_cached("gap"):
        return self.gap + 2 * self.roll.groove.depth


@TwoRollPass.contact_area
def contact_area(self: TwoRollPass):
    return 2 * self.roll.contact_area


@TwoRollPass.target_cross_section_area
def target_cross_section_area_from_target_width(self: TwoRollPass):
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section(self, self.target_width)
        return target_cross_section.area


@TwoRollPass.power
def roll_power(self: TwoRollPass):
    return 2 * self.roll.roll_power


@TwoRollPass.entry_point
def entry_point_square_oval(self: TwoRollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        depth = self.roll.groove.local_depth(self.in_profile.width / 2)
        height_change = self.in_profile.height - self.gap - 2 * depth
        radius = self.roll.max_radius - depth
        return -np.sqrt(radius * height_change - height_change ** 2 / 4)

