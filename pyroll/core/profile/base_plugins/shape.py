import math

import numpy as np
from shapely.geometry import Polygon
from shapely.ops import clip_by_rect

from ..profile import Profile


@Profile.hookimpl
def cross_section(profile: Profile) -> Polygon:
    poly = Polygon(np.concatenate([
        profile.upper_contour_line.coords,
        profile.lower_contour_line.coords
    ]))

    return clip_by_rect(poly, -profile.width / 2, -math.inf, profile.width / 2, math.inf)
