import math

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import Polygon, LineString
from shapely.ops import clip_by_rect

from ..grooves import GrooveBase
from pyroll.core.plugin_host import PluginHost


class Profile(PluginHost):
    def __init__(self, width: float, height: float, groove: GrooveBase, rotation: int = 0, **kwargs):

        self.__dict__.update(kwargs)

        super().__init__(dict(
            profile=self
        ))

        self.width = width
        self.height = height
        self.groove = groove
        self.rotation = rotation
        self._cross_section_cache = {}
        self._upper_contour_cache = {}
        self._lower_contour_cache = {}

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
        """Upper contour line edging this profile."""

        if (self.height, self.width) in self._upper_contour_cache:
            return self._upper_contour_cache[(self.height, self.width)]

        result = translate(self.groove.contour_line, yoff=self.gap / 2)
        self._upper_contour_cache[(self.height, self.width)] = result
        return result

    @property
    def lower_contour_line(self) -> LineString:
        """Lower contour line edging this profile."""

        if (self.height, self.width) in self._lower_contour_cache:
            return self._lower_contour_cache[(self.height, self.width)]

        result = rotate(self.upper_contour_line, angle=180, origin=(0, 0))
        self._lower_contour_cache[(self.height, self.width)] = result
        return result

    @property
    def perimeter(self):
        """The length of the cross-section perimeter."""
        return self.cross_section.boundary.length

    @property
    def filling_ratio(self):
        """The ratio of the profile width to the groove's usable width."""
        return self.width / self.groove.usable_width

    @property
    def gap(self):
        """Estimation of the roll gap by lowering the profile height with twice the groove depth."""
        return self.height - 2 * self.groove.depth

    def local_height(self, z):
        """Function of the local profile height in dependence on the z-coordinate."""
        return 2 * self.groove.local_depth(z) + self.height - 2 * self.groove.depth

    def __str__(self):
        return f"Profile {self.width:.4g} x {self.height:.4g} from {self.groove}"

    @property
    def types(self):
        """A tuple of keywords to specify the shape types of this profile.
        Shortcut to ``self.groove.types``."""
        return self.groove.types
