from shapely import difference, line_merge, MultiLineString

from ..base import BaseRollPass
from ...config import Config
from ...rotator import Rotator


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


@BaseRollPass.volume
def volume(self: BaseRollPass):
    return (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area
            ) / 3 * self.length


@BaseRollPass.surface_area
def surface_area(self: BaseRollPass):
    return (self.in_profile.cross_section.perimeter + 2 * self.out_profile.cross_section.perimeter
            ) / 3 * self.length


@BaseRollPass.duration
def duration(self: BaseRollPass):
    return self.length / self.velocity


@BaseRollPass.length
def length(self: BaseRollPass):
    return -self.entry_point + self.exit_point


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


@BaseRollPass.target_cross_section_area
def target_cross_section_area_from_target_cross_section_filling_ratio(self: BaseRollPass):
    if self.has_set_or_cached("target_cross_section_filling_ratio"):
        return self.target_cross_section_filling_ratio * self.usable_cross_section.area


@BaseRollPass.target_cross_section_filling_ratio
def target_cross_section_filling_ratio_from_target_cross_section_area(self: BaseRollPass):
    if self.has_value("target_cross_section_area"):  # important has_value for computing from target_width
        return self.target_cross_section_area / self.usable_cross_section.area


@BaseRollPass.exit_point
def exit_point(self: BaseRollPass):
    return 0


@BaseRollPass.Profile.contact_lines
def contact_contour_lines(self: BaseRollPass.Profile):
    rp = self.roll_pass
    contact_contur_lines_possible_multilinestring = [cl.intersection(self.cross_section.exterior.buffer(1e-9)) for cl in rp.contour_lines.geoms]

    contact_contour_lines_linestring = []
    for ccl in contact_contur_lines_possible_multilinestring:
        if isinstance(ccl, MultiLineString):
            merged_ccl = line_merge(ccl)
            contact_contour_lines_linestring.append(merged_ccl)
        else:
            contact_contour_lines_linestring.append(ccl)

    return MultiLineString(contact_contour_lines_linestring)


@BaseRollPass.front_tension
def default_front_tension(self: BaseRollPass):
    return 0


@BaseRollPass.back_tension
def default_back_tension(self: BaseRollPass):
    return 0


@BaseRollPass.technologically_orientated_contour_lines
def technologically_correctly_orientated_contour_lines(self: BaseRollPass):
    return MultiLineString([self._get_oriented_geom(cl) for cl in self.contour_lines.geoms])


@BaseRollPass.OutProfile.technologically_orientated_cross_section
def technologically_correctly_orientated_cross_section(self: BaseRollPass.OutProfile):
    return self.roll_pass._get_oriented_geom(self.cross_section, orientation=self.roll_pass.orientation)
