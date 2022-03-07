import numpy as np
import pluggy
from scipy.integrate import quad

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

    @property
    def cross_section(self):
        return 2 * quad(self.local_height, 0, self.width / 2)[0]

    @property
    def perimeter(self):
        contour_length = quad(
            lambda z: np.sqrt(1 + self.groove.contour_derivative(z) ** 2),
            0, self.width / 2
        )[0]
        return 4 * contour_length + 2 * self.local_height(self.width / 2)

    @property
    def filling_ratio(self):
        return self.width / self.groove.usable_width

    @property
    def gap(self):
        return self.height - 2 * self.groove.depth

    def local_height(self, z):
        return 2 * self.groove.contour_line(z) + self.height - 2 * self.groove.depth

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
