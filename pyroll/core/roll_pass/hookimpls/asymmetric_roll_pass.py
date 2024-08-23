import numpy as np
from shapely import Polygon

from . import helpers
from ..asymmetric_roll_pass import AsymmetricRollPass
from ...grooves import GenericElongationGroove


@AsymmetricRollPass.usable_width
def usable_width(self: AsymmetricRollPass):
    return min(self.upper_roll.groove.usable_width, self.lower_roll.groove.usable_width)


@AsymmetricRollPass.tip_width
def tip_width(self: AsymmetricRollPass):
    if isinstance(self.upper_roll.groove, GenericElongationGroove) and isinstance(
        self.lower_roll.groove, GenericElongationGroove
    ):
        return min(
            self.upper_roll.groove.usable_width + self.gap / 2 / np.tan(self.upper_roll.groove.flank_angle),
            self.lower_roll.groove.usable_width + self.gap / 2 / np.tan(self.lower_roll.groove.flank_angle),
        )


@AsymmetricRollPass.usable_cross_section
def usable_cross_section(self: AsymmetricRollPass) -> Polygon:
    return helpers.out_cross_section(self, self.usable_width)


@AsymmetricRollPass.tip_cross_section
def tip_cross_section(self: AsymmetricRollPass) -> Polygon:
    return helpers.out_cross_section(self, self.tip_width)


@AsymmetricRollPass.gap
def gap(self: AsymmetricRollPass):
    if self.has_set_or_cached("height"):
        return self.height - self.upper_roll.groove.depth - self.lower_roll.groove.depth


@AsymmetricRollPass.height
def height(self: AsymmetricRollPass):
    if self.has_set_or_cached("gap"):
        return self.gap + self.upper_roll.groove.depth + self.lower_roll.groove.depth


@AsymmetricRollPass.contact_area
def contact_area(self: AsymmetricRollPass):
    return self.upper_roll.contact_area + self.lower_roll.contact_area


@AsymmetricRollPass.target_cross_section_area
def target_cross_section_area_from_target_width(self: AsymmetricRollPass):
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section(self, self.target_width)
        return target_cross_section.area


@AsymmetricRollPass.power
def roll_power(self: AsymmetricRollPass):
    return self.upper_roll.roll_power + self.lower_roll.roll_power


@AsymmetricRollPass.entry_point
def entry_point(self: AsymmetricRollPass):
    height_change = self.in_profile.height - self.height
    return (
        np.sqrt(height_change)
        * np.sqrt(
            (2 * self.upper_roll.min_radius - height_change)
            * (2 * self.lower_roll.min_radius - height_change)
            * (2 * self.upper_roll.min_radius + 2 * self.lower_roll.min_radius - height_change)
        )
    ) / (2 * (self.upper_roll.min_radius + self.lower_roll.min_radius - height_change))


@AsymmetricRollPass.entry_point
def entry_point_square_oval(self: AsymmetricRollPass):
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


@AsymmetricRollPass.velocity
def velocity(self: AsymmetricRollPass):
    if self.upper_roll.has_value("neutral_angle") and self.lower_roll.has_value("neutral_angle"):
        return (
            self.upper_roll.working_velocity * np.cos(self.upper_roll.neutral_angle)
            + self.lower_roll.working_velocity * np.cos(self.lower_roll.neutral_angle)
        ) / 2
    else:
        return (self.upper_roll.working_velocity + self.lower_roll.working_velocity) / 2


@AsymmetricRollPass.roll_force
def roll_force(self: AsymmetricRollPass):
    return (
        (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress)
        / 3
        * (self.upper_roll.contact_area + self.lower_roll.contact_area)
        / 2
    )
