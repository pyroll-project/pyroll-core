import logging
from typing import Optional

import numpy as np
import pluggy
from scipy.integrate import quad
from ..profile import Profile
from ..grooves import GrooveBase
from ..unit import Unit


class RollPass(Unit):
    plugin_manager = pluggy.PluginManager("pyroll_roll_pass")
    hookspec = pluggy.HookspecMarker("pyroll_roll_pass")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_roll_pass")

    hooks = set()

    _hook_results_to_clear = set()

    def __init__(
            self,
            groove: GrooveBase,
            roll_radius: float,
            velocity: float,
            gap: float,
            label: str = "Roll Pass",
            **kwargs
    ):
        super().__init__(label)

        self.groove = groove
        self.roll_radius = roll_radius
        self.velocity = velocity
        self.gap = gap

        self.__dict__.update(kwargs)

        self.height = self.gap + 2 * self.groove.depth
        self.tip_width = self.groove.usable_width + self.gap / 2 / np.tan(self.groove.alpha1)

        self.usable_cross_section = 2 * quad(self.local_height, 0, self.groove.usable_width / 2)[0]
        self.tip_cross_section = 2 * quad(self.local_height, 0, self.tip_width / 2)[0]

        self.usable_mean_height = self.usable_cross_section / self.groove.usable_width
        self.usable_mean_width = self.usable_cross_section / self.height

        self.tip_mean_height = self.tip_cross_section / self.tip_width
        self.tip_mean_width = self.tip_cross_section / self.height

        self.minimal_roll_radius = self.roll_radius - self.groove.depth

        self.ideal_out_profile: Optional[RollPassOutProfile] = None

        self._log = logging.getLogger(__name__)

    def __str__(self):
        return self.label

    def __getattr__(self, key):
        if hasattr(RollPass.plugin_manager.hook, key):
            return self.get_from_hook(key)
        return super().__getattr__(key)

    def get_from_hook(self, key):
        if not hasattr(RollPass.plugin_manager.hook, key):
            return super().get_from_hook(key)

        hook = getattr(RollPass.plugin_manager.hook, key)
        result = hook(roll_pass=self)

        if result is None:
            return None

        self.__dict__[key] = result
        RollPass._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in RollPass._hook_results_to_clear:
            if key in self.__dict__:
                delattr(self, key)
        super().clear_hook_results()

    def local_height(self, z):
        return 2 * self.groove.contour_line(z) + self.gap

    def solve(self, in_profile: Profile) -> Profile:
        self._log.info(f"Started calculation of roll pass {self.label}")

        self.in_profile = RollPassInProfile(in_profile, self)
        self.in_profile.rotation = self.in_profile_rotation
        self.in_profile.clear_hook_results()

        self.out_profile = RollPassOutProfile(self, 0.95)
        self.ideal_out_profile = RollPassOutProfile(self, 1)

        old_values = np.full(len(self.hooks) + len(self.out_profile.hooks), np.nan)

        while True:
            self.clear_hook_results()
            self.out_profile.clear_hook_results()

            for key in self.hooks:
                self.get_from_hook(key)

            for key in self.out_profile.hooks:
                self.out_profile.get_from_hook(key)

            current_values = np.array(
                list(map(lambda h: getattr(self, h), self.hooks))
                +
                list(map(lambda h: getattr(self.out_profile, h), self.out_profile.hooks))
            )
            if np.all((current_values - old_values) <= old_values * 1e-2):
                break

            old_values = current_values

        return self.out_profile


class RollPassProfile(Profile):
    plugin_manager = pluggy.PluginManager("pyroll_roll_pass_profile")
    hookspec = pluggy.HookspecMarker("pyroll_roll_pass_profile")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_roll_pass_profile")

    _hook_results_to_clear = set()

    def __getattr__(self, key):
        if hasattr(RollPassProfile.plugin_manager.hook, key):
            return self.get_from_hook(key)
        return super().__getattr__(key)

    def get_from_hook(self, key):
        if not hasattr(RollPassProfile.plugin_manager.hook, key):
            return super().get_from_hook(key)
        hook = getattr(RollPassProfile.plugin_manager.hook, key)
        result = hook(roll_pass=self._roll_pass, profile=self)

        if result is None:
            return None

        self.__dict__[key] = result
        RollPassProfile._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in RollPassProfile._hook_results_to_clear:
            if key in self.__dict__:
                delattr(self, key)
        super().clear_hook_results()


class RollPassInProfile(RollPassProfile):
    def __init__(self, template: Profile, roll_pass: RollPass):
        kwargs = template.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        super().__init__(**kwargs)
        self._roll_pass = roll_pass


class RollPassOutProfile(RollPassProfile):
    plugin_manager = pluggy.PluginManager("pyroll_roll_pass_out_profile")
    hookspec = pluggy.HookspecMarker("pyroll_roll_pass_out_profile")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_roll_pass_out_profile")

    hooks = {
        "strain",
        "width",
    }

    _hook_results_to_clear = set()

    def __init__(self, roll_pass: RollPass, filling_ratio: float):
        kwargs = roll_pass.in_profile.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        kwargs.update(dict(
            width=roll_pass.groove.usable_width * filling_ratio,
            height=roll_pass.height,
            groove=roll_pass.groove,
            rotation=0,
        ))
        super().__init__(**kwargs)
        self._roll_pass = roll_pass

    def __getattr__(self, key):
        if key in self.hooks:
            return getattr(self._roll_pass.in_profile, key)
        if hasattr(RollPassOutProfile.plugin_manager.hook, key):
            return self.get_from_hook(key)
        return super().__getattr__(key)

    def get_from_hook(self, key):
        if not hasattr(RollPassOutProfile.plugin_manager.hook, key):
            return super().get_from_hook(key)
        hook = getattr(RollPassOutProfile.plugin_manager.hook, key)
        result = hook(roll_pass=self._roll_pass, profile=self)

        if result is None:
            return None

        self.__dict__[key] = result
        RollPassOutProfile._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in RollPassOutProfile._hook_results_to_clear:
            if key in self.__dict__ and key not in self.hooks:
                delattr(self, key)
        super().clear_hook_results()
