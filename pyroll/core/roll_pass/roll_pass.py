import logging
from shapely.affinity import translate, rotate
from shapely.geometry import LineString

from ..profile import Profile as BaseProfile
from ..grooves import GrooveBase
from ..unit import Unit


class RollPass(Unit):
    """Represents a roll pass."""

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
        self.hook_args["roll_pass"] = self

        self._log = logging.getLogger(__name__)

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

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)
        self.out_profile = self.OutProfile(self, 0.95)
        self.in_profile.rotation = self.in_profile_rotation

    class Profile(Unit.Profile):
        """Represents a profile in context of a roll pass."""

        def __init__(self, roll_pass: 'RollPass', template: BaseProfile):
            super().__init__(roll_pass, template)
            self.hook_args["roll_pass"] = roll_pass

    class InProfile(Profile):
        """Represents an incoming profile of a roll pass."""

        def __init__(self, roll_pass: 'RollPass', template: BaseProfile):
            super().__init__(roll_pass, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a roll pass."""

        def __init__(self, roll_pass: 'RollPass', filling_ratio: float):
            super().__init__(roll_pass, roll_pass.in_profile)
            self.width = roll_pass.groove.usable_width * filling_ratio
            self.height = roll_pass.height
            self.groove = roll_pass.groove
            self.rotation = 0


RollPass.OutProfile.root_hooks.add("width")
RollPass.root_hooks.add("roll_force")
RollPass.root_hooks.add("roll_torque")
