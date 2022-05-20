import logging
import sys

import numpy as np

from ..profile import Profile
from ...shapes import rectangle


@Profile.hookimpl
def equivalent_rectangle(profile: Profile):
    width = profile.width
    height = profile.height

    eq_width = np.sqrt(profile.cross_section.area * width / height)
    eq_height = np.sqrt(profile.cross_section.area * height / width)

    return rectangle(eq_width, eq_height)


Profile.plugin_manager.register(sys.modules[__name__])
