import numpy as np
from shapely.geometry import Polygon
from shapely.affinity import translate, rotate
from shapely.ops import linemerge

from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass

from . import helpers


@RollPass.Profile.contact_contour_lines
def contact_contour_lines(self: RollPass.Profile):
    rp = self.roll_pass
    upper_groove_cl = translate(rp.roll.contour_line, yoff=rp.gap / 2)
    lower_groove_cl = rotate(upper_groove_cl, angle=180, origin=(0, 0))

    upper_contact_contour = linemerge(upper_groove_cl.intersection(self.cross_section.exterior))
    lower_contact_contour = linemerge(lower_groove_cl.intersection(self.cross_section.exterior))

    return [upper_contact_contour, lower_contact_contour]


@RollPass.Profile.contact_contour_angles
def contact_contour_angles(self: RollPass.Profile):
    def calculate_angles(contour_line):
        angles = []
        coords = list(contour_line.coords)

        for i in range(len(coords) - 2):
            vector1 = np.array(coords[i + 1]) - np.array(coords[i])
            vector2 = np.array(coords[i + 2]) - np.array(coords[i + 1])

            dot_product = np.dot(vector1, vector2)
            magnitude1 = np.linalg.norm(vector1)
            magnitude2 = np.linalg.norm(vector2)

            cosine_angle = dot_product / (magnitude1 * magnitude2)
            angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

            angles.append(angle)
        return angles

    upper_groove_cl_angles = calculate_angles(self.contact_contour_lines[0])
    lower_groove_cl_angles = calculate_angles(self.contact_contour_lines[1])


    return [upper_groove_cl_angles, lower_groove_cl_angles]


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
    if (-cs.bounds[1] + cs.centroid.y) * 2.02 < self.width:
        raise ValueError(
            "Profile's width can not be larger than its contour lines."
            "May be caused by critical overfilling."
        )
    return cs


@RollPass.OutProfile.classifiers
def classifiers(self: RollPass.OutProfile):
    return set(self.roll_pass.classifiers)
