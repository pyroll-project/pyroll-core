import math

import numpy as np
from shapely import Polygon, clip_by_rect

from . import helpers
from ..three_roll_pass import ThreeRollPass
from ...grooves import GenericElongationGroove


@ThreeRollPass.usable_width
def usable_width3(self: ThreeRollPass) -> float:
    return 2 / 3 * np.sqrt(3) * (self.roll.groove.usable_width + self.gap / 2)


@ThreeRollPass.tip_width
def tip_width3(self: ThreeRollPass) -> float:
    if isinstance(self.roll.groove, GenericElongationGroove):
        return (
                2 / 3 * np.sqrt(3) * (self.roll.groove.usable_width + self.gap / 2)
                + self.gap / np.sqrt(3) * np.cos(self.roll.groove.flank_angle)
        )


@ThreeRollPass.usable_cross_section
def usable_cross_section3(self: ThreeRollPass) -> Polygon:
    return helpers.out_cross_section3(self, self.usable_width)


@ThreeRollPass.tip_cross_section
def tip_cross_section3(self: ThreeRollPass) -> Polygon:
    return helpers.out_cross_section3(self, self.tip_width)


@ThreeRollPass.inscribed_circle_diameter
def inscribed_circle_diameter_from_gap(self: ThreeRollPass) -> float:
    if self.has_set_or_cached("gap"):
        half = self.roll.groove.usable_width / 2 / np.sqrt(3) + self.gap / np.sqrt(3) + self.roll.groove.depth
        return half * 2


@ThreeRollPass.gap
def gap3_from_height(self: ThreeRollPass) -> float:
    if self.has_set_or_cached("height"):
        return (
                self.height / 2
                - self.roll.groove.usable_width / 2 / np.sqrt(3)
                - self.roll.groove.depth
        ) * np.sqrt(3)


@ThreeRollPass.gap
def gap3_from_icd(self: ThreeRollPass) -> float:
    if self.has_set_or_cached("inscribed_circle_diameter"):
        return (
                self.inscribed_circle_diameter / 2
                - self.roll.groove.usable_width / 2 / np.sqrt(3)
                - self.roll.groove.depth
        ) * np.sqrt(3)


@ThreeRollPass.height
def height3(self: ThreeRollPass) -> float:
    usable_contour = clip_by_rect(
        self.contour_lines.geoms[1],
        -self.roll.groove.usable_width / 2,
        -math.inf,
        self.roll.groove.usable_width / 2,
        math.inf
    )
    return abs(2 * usable_contour.bounds[1])


@ThreeRollPass.contact_area
def contact_area3(self: ThreeRollPass) -> float:
    return 3 * self.roll.contact_area


@ThreeRollPass.target_cross_section_area
def target_cross_section_area_from_target_width3(self: ThreeRollPass) -> float:
    if self.has_value("target_width"):
        target_cross_section = helpers.out_cross_section3(self, self.target_width)
        return target_cross_section.area


@ThreeRollPass.power
def roll_power_3(self: ThreeRollPass) -> float:
    return 3 * self.roll.roll_power

