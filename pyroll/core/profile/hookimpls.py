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


@Profile.equivalent_radius
def equivalent_radius(self: Profile):
    return np.sqrt(self.cross_section.area / np.pi)


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
    if hasattr(self, "thermal_conductivity") and hasattr(self, "density") and hasattr(self, "specific_heat_capacity"):
        return np.sqrt(self.thermal_conductivity * self.density * self.specific_heat_capacity)


@Profile.thermal_diffusivity
def thermal_diffusivity(self: Profile):
    if hasattr(self, "thermal_conductivity") and hasattr(self, "density") and hasattr(self, "specific_heat_capacity"):
        return self.thermal_conductivity / (self.density * self.specific_heat_capacity)



@Profile.hydrostatic_stress
def hydrostatic_stress(self: Profile):
    if hasattr(self, "longitudinal_stress") and hasattr(self, "altitudinal_stress") and hasattr(self,
                                                                                                "latitudinal_stress"):
        return (self.longitudinal_stress + self.altitudinal_stress + self.latitudinal_stress) / 3


@Profile.equivalent_stress
def equivalent_stress(self: Profile):
    if hasattr(self, "longitudinal_stress") and hasattr(self, "altitudinal_stress") and hasattr(self,
                                                                                                "latitudinal_stress"):
        return np.sqrt(1 / 2 * (self.longitudinal_stress - self.altitudinal_stress) ** 2 + (
                self.altitudinal_stress - self.latitudinal_stress) ** 2 + (
                               self.latitudinal_stress - self.longitudinal_stress) ** 2)

@Profile.astm_grain_size_number
def astm_grain_size_number(self: Profile):
    if self.has_set_or_cached("grain_size"):
        grain_diameter_inch = self.grain_size / 0.0254
        grain_area_square_inch = np.pi * (grain_diameter_inch / 2) ** 2
        grains_per_square_inch_1x_magnification = 1 / grain_area_square_inch
        grains_per_square_inch_100x_magnification = grains_per_square_inch_1x_magnification / (100 ** 2)

        return 1 + np.log2(grains_per_square_inch_100x_magnification)
