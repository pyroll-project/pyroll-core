import math

import numpy as np
import pluggy
from scipy.integrate import quad
from shapely.affinity import translate, rotate
from shapely.geometry import Polygon
from shapely.ops import polygonize, clip_by_rect

from ..grooves import GrooveBase


class Profile:
    plugin_manager = pluggy.PluginManager("pyroll_profile")
    hookspec = pluggy.HookspecMarker("pyroll_profile")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_profile")

    _hook_results_to_clear = set()

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

    @property
    def cross_section(self):
        if (self.height, self.width) in self._cross_section_cache:
            return self._cross_section_cache[(self.height, self.width)]

        poly = Polygon(np.concatenate([
            self.upper_contour_line.coords,
            self.lower_contour_line.coords
        ]))

        result = clip_by_rect(poly, -self.width / 2, -math.inf, self.width / 2, math.inf)
        self._cross_section_cache[(self.height, self.width)] = result
        return result

    @property
    def upper_contour_line(self):
        if (self.height, self.width) in self._upper_contour_cache:
            return self._upper_contour_cache[(self.height, self.width)]

        result = translate(self.groove.contour_line, yoff=self.gap / 2)
        self._upper_contour_cache[(self.height, self.width)] = result
        return result

    @property
    def lower_contour_line(self):
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

    def __getattr__(self, key):
        if hasattr(Profile.plugin_manager.hook, key):
            return self.get_from_hook(key)
        raise AttributeError(f"No attribute '{key}' or corresponding hook found!")

    def get_from_hook(self, key):
        hook = getattr(Profile.plugin_manager.hook, key)
        result = hook(profile=self)

        if result is None:
            return None

        self.__dict__[key] = result
        Profile._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in Profile._hook_results_to_clear:
            if key in self.__dict__:
                self.__dict__.pop(key, None)

    def __str__(self):
        return f"Profile {self.width:.4g} x {self.height:.4g} from {self.groove}"
