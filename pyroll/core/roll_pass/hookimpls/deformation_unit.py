import numpy as np

from shapely.ops import linemerge
from shapely.geometry import LineString
from shapely.affinity import translate, rotate

from ..roll_pass import DeformationUnit, RollPass
from ...config import Config


@DeformationUnit.draught
def draught(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.height / self.in_profile.equivalent_rectangle.height


@DeformationUnit.spread
def spread(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.width / self.in_profile.equivalent_rectangle.width


@DeformationUnit.elongation
def elongation(self: DeformationUnit):
    return self.in_profile.cross_section.area / self.out_profile.cross_section.area


@DeformationUnit.log_draught
def log_draught(self: DeformationUnit):
    return np.log(self.draught)


@DeformationUnit.log_spread
def log_spread(self: DeformationUnit):
    return np.log(self.spread)


@DeformationUnit.log_elongation
def log_elongation(self: DeformationUnit):
    return np.log(self.elongation)


@DeformationUnit.abs_draught
def abs_draught(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.height - self.in_profile.equivalent_rectangle.height


@DeformationUnit.abs_spread
def abs_spread(self: DeformationUnit):
    return self.out_profile.equivalent_rectangle.width - self.in_profile.equivalent_rectangle.width


@DeformationUnit.abs_elongation
def abs_elongation(self: DeformationUnit):
    return self.out_profile.length - self.in_profile.length


@DeformationUnit.rel_draught
def rel_draught(self: DeformationUnit):
    return self.abs_draught / self.in_profile.equivalent_rectangle.height


@DeformationUnit.rel_spread
def rel_spread(self: DeformationUnit):
    return self.abs_spread / self.in_profile.equivalent_rectangle.width


@DeformationUnit.rel_elongation
def rel_elongation(self: DeformationUnit):
    return self.abs_elongation / self.in_profile.length


@DeformationUnit.strain
def strain(self: DeformationUnit):
    return np.sqrt(2 / 3 * (self.log_elongation ** 2 + self.log_spread ** 2 + self.log_draught ** 2))


@DeformationUnit.strain_rate
def strain_rate(self: DeformationUnit):
    return np.abs(self.strain) / self.duration


@DeformationUnit.free_surface_area
def free_surface_area(self: DeformationUnit):
    return self.surface_area - self.contact_area


@DeformationUnit.zener_holomon_parameter
def zener_holomon_parameter(self: DeformationUnit):
    return self.strain_rate * np.exp(self.in_profile.deformation_activation_energy / (
            Config.UNIVERSAL_GAS_CONSTANT * self.in_profile.temperature
    ))


@DeformationUnit.Profile.contact_lines
def contact_contour_lines(self: DeformationUnit.Profile):
    if isinstance(self.unit, RollPass):
        rp = self.unit
        upper_groove_cl = translate(rp.roll.contour_line, yoff=rp.gap / 2)
        lower_groove_cl = rotate(upper_groove_cl, angle=180, origin=(0, 0))

        upper_contact_contour = linemerge(upper_groove_cl.intersection(self.cross_section.exterior))
        lower_contact_contour = linemerge(lower_groove_cl.intersection(self.cross_section.exterior))

        return [upper_contact_contour, lower_contact_contour]
    else:
        return None


@DeformationUnit.Profile.contact_angles
def contact_contour_angles(self: DeformationUnit.Profile):
    def calculate_angles(contour_line: LineString):
        x, y = np.array(contour_line.coords.xy)

        xdiff = x[2:] - x[:-2]
        ydiff = y[2:] - y[:-2]
        angles = np.arctan2(ydiff, xdiff)

        return angles

    return [calculate_angles(line) for line in self.contact_contour_lines]
