import math

import numpy as np
from shapely.ops import clip_by_rect

from ..profile import Profile
from ...shapes import Polygon


@Profile.hookimpl
def cross_section(profile: Profile) -> Polygon:
    poly = Polygon(np.concatenate([
        profile.upper_contour_line.coords,
        profile.lower_contour_line.coords
    ]))

    if (
            # one percent tolerance to bypass discretization issues
            - profile.width / 2 < poly.bounds[0] * 1.01
            or profile.width / 2 > poly.bounds[2] * 1.01
    ):
        raise ValueError("Profile's width can not be larger than its contour lines."
                         "May be caused by critical overfilling.")

    return clip_by_rect(poly, -profile.width / 2, -math.inf, profile.width / 2, math.inf)
