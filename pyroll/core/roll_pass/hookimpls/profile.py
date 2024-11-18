from shapely.geometry import Polygon

from ..base import BaseRollPass
from ..three_roll_pass import ThreeRollPass

from . import helpers


@BaseRollPass.InProfile.x
def entry_point(self: BaseRollPass.InProfile):
    return -self.roll_pass.roll.contact_length


@BaseRollPass.OutProfile.x
def exit_point(self: BaseRollPass.OutProfile):
    return 0


@BaseRollPass.InProfile.longitudinal_angle
def longitudinal_angle(self: BaseRollPass.InProfile):
    return self.roll_pass.roll.entry_angle


@BaseRollPass.OutProfile.longitudinal_angle
def longitudinal_angle(self: BaseRollPass.OutProfile):
    return self.roll_pass.roll.exit_angle


@BaseRollPass.OutProfile.strain
def strain(self: BaseRollPass.OutProfile):
    return self.roll_pass.in_profile.strain + self.roll_pass.strain


@BaseRollPass.OutProfile.width
def width(self: BaseRollPass.OutProfile):
    return self.roll_pass.usable_width


@BaseRollPass.OutProfile.length
def length(self: BaseRollPass.OutProfile):
    return self.roll_pass.elongation * self.roll_pass.in_profile.length


@BaseRollPass.OutProfile.filling_ratio
def filling_ratio(self: BaseRollPass.OutProfile):
    return self.width / self.roll_pass.usable_width


@BaseRollPass.OutProfile.cross_section_filling_ratio
def cross_section_filling_ratio(self: BaseRollPass.OutProfile):
    return self.cross_section.area / self.roll_pass.usable_cross_section.area


@BaseRollPass.OutProfile.filling_error
def filling_error(self: BaseRollPass.OutProfile):
    return self.width / self.roll_pass.target_width - 1


@BaseRollPass.OutProfile.cross_section_error
def cross_section_error(self: BaseRollPass.OutProfile):
    return self.cross_section.area / self.roll_pass.target_cross_section_area - 1


@BaseRollPass.OutProfile.cross_section
def cross_section(self: BaseRollPass.OutProfile) -> Polygon:
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
    if (cs.bounds[3] + cs.centroid.y) * 2.02 < self.width:
        raise ValueError(
            "Profile's width can not be larger than its contour lines."
            "May be caused by critical overfilling."
        )
    return cs


@BaseRollPass.OutProfile.classifiers
def classifiers(self: BaseRollPass.OutProfile):
    return set(self.roll_pass.classifiers)


@BaseRollPass.InProfile.velocity
def in_velocity(self: BaseRollPass.InProfile):
    return self.roll_pass.out_profile.velocity * self.unit.out_profile.cross_section.area / self.cross_section.area


@BaseRollPass.OutProfile.velocity
def out_velocity(self: BaseRollPass.OutProfile):
    return self.roll_pass.velocity
