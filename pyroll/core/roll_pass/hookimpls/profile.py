import math

import numpy as np
from scipy.optimize import root_scalar, fixed_point
from shapely.affinity import rotate
from shapely.geometry import Polygon
from shapely.ops import clip_by_rect

from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass

from . import helpers


@RollPass.InProfile.x
def entry_point(self: RollPass.InProfile):
    return -self.roll_pass.roll.contact_length


@RollPass.OutProfile.x
def exit_point(self: RollPass.OutProfile):
    return 0


@RollPass.OutProfile.strain
def strain(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.strain + self.roll_pass.strain


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    return self.roll_pass.usable_width


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile, cycle):
    if cycle:
        return None

    if self.has_set("equivalent_width"):
        def w(x):
            return self.equivalent_width ** 2 / helpers.out_cross_section(self.roll_pass, x).area * self.height

        return fixed_point(w, x0=self.width)


@RollPass.OutProfile.length
def length(self: RollPass.OutProfile):
    return self.roll_pass.elongation * self.roll_pass.in_profile.length


@RollPass.OutProfile.filling_ratio
def filling_ratio(self: RollPass.OutProfile):
    return self.width / self.roll_pass.usable_width


@RollPass.OutProfile.cross_section_filling_ratio
def cross_section_filling_ratio(self: RollPass.OutProfile):
    return self.cross_section.area / self.roll_pass.usable_cross_section.area


@RollPass.OutProfile.filling_error
def filling_error(self: RollPass.OutProfile):
    return self.width / self.roll_pass.target_width - 1


@RollPass.OutProfile.cross_section_error
def cross_section_error(self: RollPass.OutProfile):
    return self.cross_section.area / self.roll_pass.target_cross_section_area - 1


@RollPass.OutProfile.cross_section
def cross_section(self: RollPass.OutProfile) -> Polygon:
    cs = helpers.out_cross_section(self.roll_pass, self.width)
    if cs.width * 1.01 < self.width:
        raise ValueError(
            "Profile's width can not be larger than its contour lines."
            "May be caused by critical overfilling."
        )
    return cs


@ThreeRollPass.OutProfile.cross_section
def cross_section3(self: ThreeRollPass.OutProfile) -> Polygon:
    cs = helpers.out_cross_section3(self.roll_pass, self.width)
    if (cs.bounds[3] - cs.centroid.y) * 2.02 < self.width:
        raise ValueError(
            "Profile's width can not be larger than its contour lines."
            "May be caused by critical overfilling."
        )
    return cs


@RollPass.OutProfile.classifiers
def classifiers(self: RollPass.OutProfile):
    return set(self.roll_pass.classifiers)
