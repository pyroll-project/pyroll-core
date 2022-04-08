import logging

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString

from ..profile import Profile
from ..grooves import GrooveBase
from ..unit import Unit
from ..plugin_host import PluginHost


class RollPass(Unit, metaclass=PluginHost):
    """Represents a roll pass."""

    hooks = set()
    """Set of hooks to call in every solution iteration."""

    def __init__(
            self,
            groove: GrooveBase,
            label: str = "Roll Pass",
            **kwargs
    ):
        super().__init__(label)

        self.groove = groove
        """Groove of this pass' rolls."""

        self.__dict__.update(kwargs)

        self._log = logging.getLogger(__name__)
        self.hook_args = dict(
            roll_pass=self
        )

    def __str__(self):
        return "RollPass {label}with {groove}".format(
            label=f"'{self.label}' " if self.label else "",
            groove=self.groove
        )

    def local_height(self, z):
        """Local height of the roll gap in dependence on z."""
        return 2 * self.groove.local_depth(z) + self.gap

    @property
    def upper_contour_line(self) -> LineString:
        """Contour line object of the upper working roll."""
        return translate(self.groove.contour_line, yoff=self.gap / 2)

    @property
    def lower_contour_line(self) -> LineString:
        """Contour line object of the lower working roll."""
        return rotate(self.upper_contour_line, angle=180, origin=(0, 0))

    @property
    def types(self):
        """A tuple of keywords to specify the shape types of this roll pass.
        Shortcut to ``self.groove.types``."""
        return self.groove.types

    def solve(self, in_profile: Profile) -> Profile:
        self._log.info(f"Started calculation of roll pass {self.label}")

        self.in_profile = RollPassInProfile(self, in_profile)
        self.out_profile = RollPassOutProfile(self, 0.95)
        self.in_profile.rotation = self.in_profile_rotation
        self.in_profile.clear_hook_results()

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


class RollPassProfile(Profile, metaclass=PluginHost):
    """Represents a profile in context of a roll pass."""
    def __init__(self, roll_pass, **kwargs):
        super().__init__(**kwargs)
        self.hook_args = dict(
            profile=self,
            roll_pass=roll_pass
        )


class RollPassInProfile(RollPassProfile, metaclass=PluginHost):
    """Represents an incoming profile of a roll pass."""
    def __init__(self, roll_pass: RollPass, template: Profile):
        kwargs = template.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        super().__init__(roll_pass, **kwargs)


class RollPassOutProfile(RollPassProfile, metaclass=PluginHost):
    """Represents an outgoing profile of a roll pass."""
    hooks = {
        "strain",
        "width",
    }
    """Set of hooks to call in every solution iteration."""

    def __init__(self, roll_pass: RollPass, filling_ratio: float):
        kwargs = roll_pass.in_profile.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        kwargs.update(dict(
            width=roll_pass.groove.usable_width * filling_ratio,
            height=roll_pass.height,
            groove=roll_pass.groove,
            rotation=0,
        ))
        super().__init__(roll_pass, **kwargs)
