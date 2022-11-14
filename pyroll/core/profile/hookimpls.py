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


@Profile.equivalent_rectangle
def equivalent_rectangle(self: Profile):
    width = self.width
    height = self.height

    eq_width = np.sqrt(self.cross_section.area * width / height)
    eq_height = np.sqrt(self.cross_section.area * height / width)

    return rectangle(eq_width, eq_height)
