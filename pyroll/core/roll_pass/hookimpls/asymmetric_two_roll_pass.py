import numpy as np
from shapely import Polygon

from . import helpers
from ..asymmetric_two_roll_pass import AsymmetricTwoRollPass
from ...grooves import GenericElongationGroove


@AsymmetricTwoRollPass.usable_width
def usable_width(self: AsymmetricTwoRollPass):
    return min(self.upper_roll.groove.usable_width, self.lower_roll.groove.usable_width)


@AsymmetricTwoRollPass.tip_width
def tip_width(self: AsymmetricTwoRollPass):
    if isinstance(self.upper_roll.groove, GenericElongationGroove) and isinstance(
        self.lower_roll.groove, GenericElongationGroove
    ):
        return min(
            self.upper_roll.groove.usable_width + self.gap / 2 / np.tan(self.upper_roll.groove.flank_angle),
            self.lower_roll.groove.usable_width + self.gap / 2 / np.tan(self.lower_roll.groove.flank_angle),
        )


@AsymmetricTwoRollPass.usable_cross_section
def usable_cross_section(self: AsymmetricTwoRollPass) -> Polygon:
    return helpers.out_cross_section(self, self.usable_width)


@AsymmetricTwoRollPass.tip_cross_section
def tip_cross_section(self: AsymmetricTwoRollPass) -> Polygon:
    return helpers.out_cross_section(self, self.tip_width)


@AsymmetricTwoRollPass.gap
def gap(self: AsymmetricTwoRollPass):
    if self.has_set_or_cached("height"):
        return self.height - self.upper_roll.groove.depth - self.lower_roll.groove.depth


@AsymmetricTwoRollPass.height
def height(self: AsymmetricTwoRollPass):
    if self.has_set_or_cached("gap"):
        return self.gap + self.upper_roll.groove.depth + self.lower_roll.groove.depth


@AsymmetricTwoRollPass.contact_area
def contact_area(self: AsymmetricTwoRollPass):
    return self.upper_roll.contact_area + self.lower_roll.contact_area


@AsymmetricTwoRollPass.target_cross_section_area
def target_cross_section_area_from_target_width(self: AsymmetricTwoRollPass):
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section(self, self.target_width)
        return target_cross_section.area


@AsymmetricTwoRollPass.power
def roll_power(self: AsymmetricTwoRollPass):
    return self.upper_roll.roll_power + self.lower_roll.roll_power


@AsymmetricTwoRollPass.entry_point
def entry_point(self: AsymmetricTwoRollPass):
    height_change = self.in_profile.height - self.height
    return (
        np.sqrt(height_change)
        * np.sqrt(
            (2 * self.upper_roll.min_radius - height_change)
            * (2 * self.lower_roll.min_radius - height_change)
            * (2 * self.upper_roll.min_radius + 2 * self.lower_roll.min_radius - height_change)
        )
    ) / (2 * (self.upper_roll.min_radius + self.lower_roll.min_radius - height_change))


@AsymmetricTwoRollPass.entry_point
def entry_point_square_oval(self: AsymmetricTwoRollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        upper_depth = self.upper_roll.groove.local_depth(self.in_profile.width / 2)
        lower_depth = self.lower_roll.groove.local_depth(self.in_profile.width / 2)
        height_change = self.in_profile.height - self.gap - upper_depth - lower_depth
        upper_radius = self.upper_roll.max_radius - upper_depth
        lower_radius = self.lower_roll.max_radius - lower_depth
        return (
                np.sqrt(height_change)
                * np.sqrt(
            (2 * upper_radius - height_change)
            * (2 * lower_radius - height_change)
            * (2 * upper_radius + 2 * lower_radius - height_change)
        )
        ) / (2 * (upper_radius + lower_radius - height_change))


@AsymmetricTwoRollPass.velocity
def velocity(self: AsymmetricTwoRollPass):
    if self.upper_roll.has_value("neutral_angle") and self.lower_roll.has_value("neutral_angle"):
        return (
            self.upper_roll.working_velocity * np.cos(self.upper_roll.neutral_angle)
            + self.lower_roll.working_velocity * np.cos(self.lower_roll.neutral_angle)
        ) / 2
    else:
        return (self.upper_roll.working_velocity + self.lower_roll.working_velocity) / 2


@AsymmetricTwoRollPass.roll_force
def roll_force(self: AsymmetricTwoRollPass):
    return (
        (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress)
        / 3
        * (self.upper_roll.contact_area + self.lower_roll.contact_area)
        / 2
    )
