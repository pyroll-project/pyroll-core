import numpy as np

from .roll import Roll
from ..config import GROOVE_PADDING


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
    return self.roll_torque * self.rotational_frequency


@Roll.surface_velocity
def surface_velocity(self: Roll):
    return self.rotational_frequency * self.nominal_radius


@Roll.rotational_frequency
def rotational_frequency(self: Roll):
    return self.surface_velocity / self.nominal_radius


@Roll.width
def width(self: Roll):
    return self.groove.width * (1 + 2 * GROOVE_PADDING)


@Roll.contour_points
def contour_points(self: Roll):
    points = np.zeros((len(self.groove.contour_points) + 2, 2), dtype=float)
    points[1:-1] = self.groove.contour_points

    z_max = self.groove.width * (0.5 + GROOVE_PADDING)
    points[0, 0] = -z_max
    points[-1, 0] = z_max

    return points


@Roll.surface_x
def surface_x(self: Roll):
    half_pi = np.pi / 2
    return -self.min_radius * np.sin(np.linspace(-half_pi, half_pi, 100))


@Roll.surface_z
def surface_z(self: Roll):
    return self.contour_points[:, 0]


@Roll.surface_y
def surface_y(self: Roll):
    local_radii = self.max_radius - self.contour_points[:, 1]
    return self.max_radius - np.sqrt(local_radii ** 2 - self.surface_x.reshape(-1, 1) ** 2)
