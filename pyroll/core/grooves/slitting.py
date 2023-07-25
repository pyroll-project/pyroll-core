from typing import Union

import numpy as np
from numpy import tan, sin
from shapely.geometry import LineString, Polygon

from .base import GrooveBase
from .generic_elongation import GenericElongationGroove


class SlittingGroove(GrooveBase):

    def __init__(
            self,
            template_groove_type: type,
            separator_indent: float,
            **kwargs
    ):
        self._outer_groove = template_groove_type(**kwargs)
        self._inner_groove = template_groove_type(
            **(kwargs | dict(pad=0, rel_pad=0, pad_angle=0, depth=self._outer_groove.depth - separator_indent))
        )

        self.z_pass = -self._inner_groove.contour_points[0, 0]

        outer_right_side = self._outer_groove.contour_points[self._outer_groove.contour_points[:, 0] >= 0].copy()
        outer_right_side[:, 0] += self.z_pass
        inner_right_side = self._inner_groove.contour_points[self._inner_groove.contour_points[:, 0] <= 0].copy()
        inner_right_side[:, 0] += self.z_pass
        inner_right_side[:, 1] += separator_indent
        right_side = np.concatenate([inner_right_side[:-1], outer_right_side])

        left_side = right_side[1:].copy()
        left_side[:, 0] *= -1

        self._contour_points = np.concatenate([left_side[::-1], right_side])
        self._contour_line = LineString(self._contour_points)
        self._cross_section = Polygon(self._contour_line)

        self._classifiers = set(self._outer_groove.classifiers)

        self.test_plausibility()

    @property
    def contour_points(self):
        return self._contour_points

    @property
    def contour_line(self) -> LineString:
        return self._contour_line

    @property
    def cross_section(self) -> Polygon:
        return self._cross_section

    def local_depth(self, z) -> Union[float, np.ndarray]:
        z = np.abs(z)

        return np.piecewise(
            z,
            [np.abs(z) < self.z_pass, np.abs(z) >= self.z_pass],
            [self._inner_groove.local_depth, self._outer_groove.local_depth]
        )

    @property
    def classifiers(self):
        return {"slitting"} | self._classifiers

    @property
    def usable_width(self) -> float:
        return self._outer_groove.usable_width / 2 + self.z_pass

    @property
    def width(self) -> float:
        return self._outer_groove.z1 + self.z_pass

    @property
    def depth(self) -> float:
        return self._outer_groove.depth

    def test_plausibility(self):
        pass

    @property
    def __attrs__(self):
        return {
            n: v for n in ["depth", "separator_indent",
                           "usable_width", "classifiers", "pad_angle",
                           "contour_line"]
            if (v := getattr(self, n))
        }
