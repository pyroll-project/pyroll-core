import math

import numpy as np
from shapely.ops import clip_by_rect

from ..profile import Profile
from ...shapes import Polygon


@Profile.cross_section
def cross_section(self: Profile) -> Polygon:
    poly = Polygon(np.concatenate([
        self.upper_contour_line.coords,
        self.lower_contour_line.coords
    ]))

    if (
            # one percent tolerance to bypass discretization issues
            - self.width / 2 < poly.bounds[0] * 1.01
            or self.width / 2 > poly.bounds[2] * 1.01
    ):
        raise ValueError("Profile's width can not be larger than its contour lines."
                         "May be caused by critical overfilling.")

    return clip_by_rect(poly, -self.width / 2, -math.inf, self.width / 2, math.inf)
