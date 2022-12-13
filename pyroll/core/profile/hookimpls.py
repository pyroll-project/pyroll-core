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


@Profile.length
def length(self: Profile):
    return 0


@Profile.equivalent_height
def equivalent_height(self: Profile):
    return np.sqrt(self.cross_section.area * self.height / self.width)


@Profile.equivalent_height
def equivalent_height(self: Profile):
    if self.has_set_or_cached("equivalent_rectangle"):
        return self.equivalent_rectangle.height


@Profile.equivalent_width
def equivalent_width(self: Profile):
    return np.sqrt(self.cross_section.area * self.width / self.height)


@Profile.equivalent_width
def equivalent_width(self: Profile):
    if self.has_set_or_cached("equivalent_rectangle"):
        return self.equivalent_rectangle.width


@Profile.equivalent_rectangle
def equivalent_rectangle(self: Profile):
    return rectangle(self.equivalent_width, self.equivalent_height)


@Profile.surface_temperature
def surface_temperature(self: Profile):
    return self.temperature


@Profile.core_temperature
def core_temperature(self: Profile):
    return self.temperature
