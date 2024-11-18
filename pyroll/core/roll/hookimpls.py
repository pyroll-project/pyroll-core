import numpy as np

from .roll import Roll
from ..config import Config


@Roll.working_radius
def working_radius(self: Roll):
    return self.nominal_radius - self.contour_line.centroid.y


@Roll.min_radius
def min_radius(self: Roll):
    return self.max_radius - self.contour_line.bounds[3]


@Roll.max_radius
def max_radius(self: Roll):
    return self.nominal_radius


@Roll.roll_power
def roll_power(self: Roll):
    return self.roll_torque * self.rotational_frequency * 2 * np.pi


@Roll.working_velocity
def working_velocity(self: Roll, cycle):
    if not cycle:
        return self.rotational_frequency * self.working_radius * 2 * np.pi


@Roll.surface_velocity
def surface_velocity(self: Roll, cycle):
    if not cycle:
        return self.rotational_frequency * self.nominal_radius * 2 * np.pi


@Roll.rotational_frequency
def rotational_frequency(self: Roll, cycle):
    if not cycle:
        return self.surface_velocity / (2 * np.pi * self.nominal_radius)


@Roll.rotational_frequency
def rotational_frequency(self: Roll, cycle):
    if not cycle:
        return self.working_velocity / (2 * np.pi * self.working_radius)


@Roll.width
def width(self: Roll):
    return self.groove.width


@Roll.contour_points
def contour_points(self: Roll):
    return self.groove.contour_points


@Roll.surface_x
def surface_x(self: Roll):
    padded_contact_angle = np.arcsin(1.1 * self.contact_length / self.min_radius) if self.has_set_or_cached("contact_length") else np.pi / 4
    points = np.concatenate([
        np.linspace(0, padded_contact_angle, Config.ROLL_SURFACE_DISCRETIZATION_COUNT, endpoint=False),
        np.linspace(padded_contact_angle, np.pi / 2, Config.ROLL_SURFACE_DISCRETIZATION_COUNT),
    ])
    return self.min_radius * np.sin(np.concatenate([-points[::-1], points[1:]]))


@Roll.surface_z
def surface_z(self: Roll):
    return self.contour_points[:, 0]


@Roll.surface_y
def surface_y(self: Roll):
    local_radii = self.max_radius - self.contour_points[:, 1]
    return self.max_radius - np.sqrt(local_radii.reshape(-1, 1) ** 2 - self.surface_x ** 2)


@Roll.heat_penetration_number
def heat_penetration_number(self: Roll):
    if hasattr(self, "thermal_conductivity") and hasattr(self, "density") and hasattr(self, "specific_heat_capacity"):
        return np.sqrt(self.thermal_conductivity * self.density * self.specific_heat_capacity)


@Roll.thermal_diffusivity
def thermal_diffusivity(self: Roll):
    if hasattr(self, "thermal_conductivity") and hasattr(self, "density") and hasattr(self, "specific_heat_capacity"):
        return self.thermal_conductivity / (self.density * self.specific_heat_capacity)


@Roll.nominal_radius
def nominal_radius(self: Roll):
    if self.has_set("nominal_diameter"):
        return self.nominal_diameter / 2


@Roll.nominal_diameter
def nominal_diameter(self: Roll):
    if self.has_set("nominal_radius"):
        return self.nominal_radius * 2
