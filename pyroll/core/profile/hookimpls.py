import numpy as np

from .profile import Profile
from ..shapes import rectangle


@Profile.height
def height(self: Profile):
    if hasattr(self, "cross_section"):
        return np.abs(self.cross_section.bounds[3] - self.cross_section.bounds[1])


@Profile.width
def width(self: Profile):
    if hasattr(self, "cross_section"):
        return np.abs(self.cross_section.bounds[2] - self.cross_section.bounds[0])


@Profile.height
def height_3fold(self: Profile):
    if "3fold" in self.classifiers:
        return (self.cross_section.centroid.y - self.cross_section.bounds[1]) * 2


@Profile.width
def width_3fold(self: Profile):
    if "3fold" in self.classifiers:
        return (self.cross_section.bounds[3] - self.cross_section.centroid.y) * 2


@Profile.equivalent_height
def equivalent_height(self: Profile):
    return np.sqrt(self.cross_section.area * self.height / self.width)


@Profile.equivalent_width
def equivalent_width(self: Profile):
    return np.sqrt(self.cross_section.area * self.width / self.height)


@Profile.equivalent_rectangle
def equivalent_rectangle(self: Profile):
    return rectangle(self.equivalent_width, self.equivalent_height)


@Profile.surface_temperature
def surface_temperature(self: Profile):
    return self.temperature


@Profile.core_temperature
def core_temperature(self: Profile):
    return self.temperature


@Profile.heat_penetration_number
def heat_penetration_number(self: Profile):
    if hasattr(self, "thermal_conductivity") and hasattr(self, "density") and hasattr(self, "thermal_capacity"):
        return np.sqrt(self.thermal_conductivity * self.density * self.thermal_capacity)


@Profile.thermal_diffusivity
def thermal_diffusivity(self: Profile):
    if hasattr(self, "thermal_conductivity") and hasattr(self, "density") and hasattr(self, "thermal_capacity"):
        return self.thermal_conductivity / (self.density * self.thermal_capacity)
