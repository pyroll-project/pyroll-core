import math

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import Polygon, LineString
from shapely.ops import clip_by_rect

from ..grooves import GrooveBase
from pyroll.core.plugin_host import PluginHost


class Profile(metaclass=PluginHost):
    def __init__(
            self,
            width: float,
            height: float,
            groove: GrooveBase,
            rotation: int = 0,
            **kwargs
    ):
        self.__dict__.update(kwargs)

        self.width = width
        self.height = height
        self.groove = groove
        self.rotation = rotation
        self._cross_section_cache = {}
        self._upper_contour_cache = {}
        self._lower_contour_cache = {}

        self.hook_args = dict(
            profile=self
        )

    @property
    def cross_section(self) -> Polygon:
        """Polygon object representing the cross-section of the profile."""
        if (self.height, self.width) in self._cross_section_cache:
            return self._cross_section_cache[(self.height, self.width)]

        poly = Polygon(np.concatenate([
            self.upper_contour_line.coords,
            self.lower_contour_line.coords
        ]))

        clipped = clip_by_rect(poly, -self.width / 2, -math.inf, self.width / 2, math.inf)
        rotated = rotate(clipped, origin=(0, 0), angle=self.rotation)
        self._cross_section_cache[(self.height, self.width)] = rotated
        return rotated

    @property
    def upper_contour_line(self) -> LineString:
        """"""
        if (self.height, self.width) in self._upper_contour_cache:
            return self._upper_contour_cache[(self.height, self.width)]

        result = translate(self.groove.contour_line, yoff=self.gap / 2)
        self._upper_contour_cache[(self.height, self.width)] = result
        return result

    @property
    def lower_contour_line(self) -> LineString:
        if (self.height, self.width) in self._lower_contour_cache:
            return self._lower_contour_cache[(self.height, self.width)]

        result = rotate(self.upper_contour_line, angle=180, origin=(0, 0))
        self._lower_contour_cache[(self.height, self.width)] = result
        return result

    @property
    def perimeter(self):
        return self.cross_section.boundary.length

    @property
    def filling_ratio(self):
        return self.width / self.groove.usable_width

    @property
    def gap(self):
        return self.height - 2 * self.groove.depth

    def local_height(self, z):
        return 2 * self.groove.local_depth(z) + self.height - 2 * self.groove.depth

    def __str__(self):
        return f"Profile {self.width:.4g} x {self.height:.4g} from {self.groove}"
