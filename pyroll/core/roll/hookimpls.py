import numpy as np

from .roll import Roll


@Roll.working_radius
def working_radius(self: Roll):
    return self.nominal_radius - self.contour_line.centroid.y


@Roll.min_radius
def min_radius(self: Roll):
    return self.max_radius - self.contour_line.bounds[3]


@Roll.max_radius
def max_radius(self: Roll):
    return self.nominal_radius


@Roll.contour_line
def contour_line(self: Roll):
    return self.groove.contour_line


@Roll.roll_power
def roll_power(self: Roll):
    return self.roll_torque * self.rotational_frequency


@Roll.surface_velocity
def surface_velocity(self: Roll):
    return self.rotational_frequency * self.nominal_radius


@Roll.rotational_frequency
def rotational_frequency(self: Roll):
    return self.surface_velocity / self.nominal_radius