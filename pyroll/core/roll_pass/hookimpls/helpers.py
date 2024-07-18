import math

import numpy as np
from shapely import Polygon, clip_by_rect
from shapely.affinity import rotate

from ..roll_pass import RollPass
from ..three_roll_pass import ThreeRollPass
from ...profile.profile import refine_cross_section


def out_cross_section(rp: RollPass, width: float) -> Polygon:
    poly = Polygon(np.concatenate([cl.coords for cl in rp.contour_lines]))
    return refine_cross_section(clip_by_rect(poly, -width / 2, -math.inf, width / 2, math.inf))


def out_cross_section3(rp: ThreeRollPass, width: float) -> Polygon:
    poly = Polygon(np.concatenate([cl.coords for cl in rp.contour_lines]))

    for _ in range(3):
        poly = clip_by_rect(poly, -math.inf, -math.inf, math.inf, width / 2)
        poly = rotate(poly, angle=120, origin=(0, 0))

    return refine_cross_section(poly)
