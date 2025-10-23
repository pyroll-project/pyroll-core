import math

import numpy as np
import shapely
from shapely import Polygon, clip_by_rect
from shapely.affinity import rotate

from ..two_roll_pass import TwoRollPass
from ..three_roll_pass import ThreeRollPass
from ...profile.profile import refine_cross_section


def out_cross_section(rp: TwoRollPass, width: float) -> Polygon:
    poly = Polygon(np.concatenate([cl.coords for cl in rp.contour_lines.geoms]))
    poly = clip_by_rect(poly, -width / 2, -math.inf, width / 2, math.inf)
    return refine_cross_section(poly)


def out_cross_section3(rp: ThreeRollPass, width: float) -> Polygon:
    poly = Polygon(np.concatenate([cl.coords for cl in rp.contour_lines.geoms]))

    for _ in range(3):
        poly = clip_by_rect(poly, -math.inf, -math.inf, math.inf, width / 2)
        poly = rotate(poly, angle=120, origin=(0, 0))

    return refine_cross_section(poly)
