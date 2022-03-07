import logging
import sys

import numpy as np

from ..profile import Profile
from ...dimensions import Dimensions


@Profile.hookimpl
def equivalent_rectangle(profile: Profile):
    width = profile.rotated.width
    height = profile.rotated.height

    eq_width = np.sqrt(profile.cross_section * width / height)
    eq_height = np.sqrt(profile.cross_section * height / width)

    return Dimensions(eq_width, eq_height)


Profile.plugin_manager.register(sys.modules[__name__])
