import math

import numpy as np
from shapely.geometry import Polygon
from shapely.ops import clip_by_rect

from ..roll_pass import RollPass


@RollPass.InProfile.x
def entry_point(self: RollPass.InProfile):
    return -self.roll_pass().roll.contact_length


@RollPass.OutProfile.x
def exit_point(self: RollPass.OutProfile):
    return 0


@RollPass.OutProfile.strain
def strain(self: RollPass.OutProfile):
    return self.roll_pass().in_profile.strain + self.roll_pass().log_elongation


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    return self.roll_pass().roll.groove.usable_width


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    if self.has_set_or_cached("cross_section") and self.has_set_or_cached("equivalent_width"):
        return self.equivalent_width ** 2 / self.cross_section.area * self.height


@RollPass.OutProfile.length
def length(self: RollPass.OutProfile):
    return self.roll_pass().elongation * self.roll_pass().in_profile.length


@RollPass.OutProfile.filling_ratio
def filling_ratio(self: RollPass.OutProfile):
    return self.width / self.roll_pass().roll.groove.usable_width


@RollPass.OutProfile.cross_section
def cross_section(self: RollPass.OutProfile) -> Polygon:
    poly = Polygon(np.concatenate([
        self.roll_pass().upper_contour_line.coords,
        self.roll_pass().lower_contour_line.coords
    ]))

    if (
            # one percent tolerance to bypass discretization issues
            - self.width / 2 < poly.bounds[0] * 1.01
            or self.width / 2 > poly.bounds[2] * 1.01
    ):
        raise ValueError("Profile's width can not be larger than its contour lines."
                         "May be caused by critical overfilling.")

    return clip_by_rect(poly, -self.width / 2, -math.inf, self.width / 2, math.inf)
