import numpy as np

from ..profile import Profile
from ...shapes import rectangle


@Profile.equivalent_rectangle
def equivalent_rectangle(self: Profile):
    width = self.width
    height = self.height

    eq_width = np.sqrt(self.cross_section.area * width / height)
    eq_height = np.sqrt(self.cross_section.area * height / width)

    return rectangle(eq_width, eq_height)
