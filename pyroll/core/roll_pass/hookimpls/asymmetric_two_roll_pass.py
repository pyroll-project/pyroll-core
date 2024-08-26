import numpy as np
import scipy.optimize
import shapely.affinity
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


@AsymmetricTwoRollPass.InProfile.pass_line
def pass_line(self: AsymmetricTwoRollPass.InProfile) -> tuple[float, float, float]:
    rp = self.roll_pass

    if not self.has_set("pass_line"):
        height_change = self.height - rp.height
        x_guess = -(
            np.sqrt(height_change)
            * np.sqrt(
                (2 * rp.upper_roll.min_radius - height_change)
                * (2 * rp.lower_roll.min_radius - height_change)
                * (2 * rp.upper_roll.min_radius + 2 * rp.lower_roll.min_radius - height_change)
            )
        ) / (2 * (rp.upper_roll.min_radius + rp.lower_roll.min_radius - height_change))
        y_guess = 0
    else:
        x_guess, y_guess, _ = self.pass_line

    def contact_objective(xy):
        shifted_cross_section = shapely.affinity.translate(rp.rotated_in_profile.cross_section, yoff=xy[1])

        upper_contour = shapely.geometry.LineString(np.stack([
            rp.upper_roll.surface_z,
            rp.upper_roll.surface_interpolation(xy[0], rp.upper_roll.surface_z).squeeze(axis=1)
        ], axis=1))
        upper_contour = shapely.affinity.translate(upper_contour,yoff=self.roll_pass.gap / 2)
        lower_contour = shapely.geometry.LineString(np.stack([
            rp.lower_roll.surface_z,
            rp.lower_roll.surface_interpolation(xy[0], rp.lower_roll.surface_z).squeeze(axis=1)
        ], axis=1))
        lower_contour = shapely.affinity.scale(shapely.affinity.translate(lower_contour, yoff=self.roll_pass.gap / 2), xfact=1, yfact=-1, origin=(0,0))

        upper_intersection = shapely.intersection(upper_contour, shifted_cross_section)
        lower_intersection = shapely.intersection(lower_contour, shifted_cross_section)

        upper_value = upper_intersection.length if not upper_intersection.is_empty else shapely.shortest_line(upper_contour, shifted_cross_section).length
        lower_value = lower_intersection.length if not lower_intersection.is_empty else shapely.shortest_line(lower_contour, shifted_cross_section).length

        return upper_value ** 2 + lower_value ** 2

    sol = scipy.optimize.minimize(contact_objective, (x_guess, y_guess), method="BFGS", options=dict(xrtol=1e-2))

    return sol.x[0], sol.x[1], 0


@AsymmetricTwoRollPass.InProfile.cross_section
def in_cross_section(self:AsymmetricTwoRollPass.InProfile):
    return shapely.affinity.translate(self.roll_pass.rotated_in_profile.cross_section, xoff=self.pass_line[2], yoff=self.pass_line[1])


@AsymmetricTwoRollPass.entry_point
def entry_point(self: AsymmetricTwoRollPass):
    return self.in_profile.pass_line[0]

