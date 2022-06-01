import logging
import math

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, Polygon
from shapely.ops import clip_by_rect

from ..roll import Roll as BaseRoll
from ..profile import Profile as BaseProfile
from ..shapes import linemerge_if_multi
from ..unit import Unit


class RollPass(Unit):
    """Represents a roll pass."""

    def __init__(
            self,
            roll: BaseRoll,
            label: str = "Roll Pass",
            **kwargs
    ):
        super().__init__(label)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (equal upper and lower)."""
        self.roll.roll_pass = self

        self.__dict__.update(kwargs)
        self.hook_args["roll_pass"] = self

        self._log = logging.getLogger(__name__)

    def local_height(self, z: float) -> float:
        coords = np.array([(1, -1), (1, 1)]) * (z, self.height)

        vline = LineString(
            coords
        )

        poly = Polygon(np.concatenate([
            self.upper_contour_line.coords,
            self.lower_contour_line.coords
        ]))

        intersection = vline.intersection(poly)

        return intersection.length

    def __str__(self):
        return f"RollPass '{self.label}'"

    @property
    def upper_contour_line(self) -> LineString:
        """Contour line object of the upper working roll."""
        return translate(self.roll.contour_line, yoff=self.gap / 2)

    @property
    def lower_contour_line(self) -> LineString:
        """Contour line object of the lower working roll."""
        return rotate(self.upper_contour_line, angle=180, origin=(0, 0))

    @property
    def types(self):
        """A tuple of keywords to specify the shape types of this roll pass.
        Shortcut to ``self.groove.types``."""
        return self.roll.groove.types

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)
        self.out_profile = self.OutProfile(self, 0.95)

        rotated_cross_section = rotate(in_profile.cross_section, angle=self.in_profile_rotation, origin=(0, 0))

        self.in_profile.upper_contour_line = linemerge_if_multi(
            clip_by_rect(rotated_cross_section.exterior, -math.inf, 0, math.inf, math.inf)
        )

        self.in_profile.lower_contour_line = linemerge_if_multi(
            clip_by_rect(rotated_cross_section.exterior, -math.inf, -math.inf, math.inf, 0)
        )

        self.in_profile.width = rotated_cross_section.bounds[2] - rotated_cross_section.bounds[0]
        self.in_profile.height = rotated_cross_section.bounds[3] - rotated_cross_section.bounds[1]
        self.in_profile.delete_hook_result_attributes()

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.get_root_hook_results()

        return np.concatenate([super_results, roll_results], axis=0)

    def delete_hook_result_attributes(self):
        super().delete_hook_result_attributes()
        self.roll.delete_hook_result_attributes()

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
            self.width = roll_pass.roll.groove.usable_width * filling_ratio
            self.height = roll_pass.height
            self.upper_contour_line = roll_pass.upper_contour_line
            self.lower_contour_line = roll_pass.lower_contour_line
            self.rotation = 0
            self.types = roll_pass.types

    class Roll(BaseRoll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: 'RollPass'):
            kwargs = template.__dict__.copy()
            kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
            super().__init__(**kwargs)
            self.hook_args["roll_pass"] = roll_pass


RollPass.OutProfile.root_hooks.add("width")
RollPass.OutProfile.root_hooks.add("strain")
RollPass.root_hooks.add("roll_force")
RollPass.Roll.root_hooks.add("roll_torque")
