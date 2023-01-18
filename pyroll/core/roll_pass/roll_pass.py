import logging
import weakref
from typing import List, cast

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, Polygon

from ..disk_element import DiskedUnit
from ..hooks import Hook
from ..profile import Profile as BaseProfile
from ..roll import Roll as BaseRoll
from ..rotator import Rotator
from .deformation_unit import DeformationUnit


class RollPass(DiskedUnit, DeformationUnit):
    """Represents a roll pass."""

    in_profile_rotation = Hook[float]()
    """Rotation applied to the incoming profile in ° (degree)."""

    gap = Hook[float]()
    """Gap between the rolls (outer surface)."""

    height = Hook[float]()
    """Maximum height of the roll pass."""

    tip_width = Hook[float]()
    """Width of the intersection of the extended groove flanks (theoretical maximum filling width)."""

    roll_force = Hook[float]()
    """Vertical roll force."""

    def __init__(
            self,
            roll: BaseRoll,
            label: str = "",
            **kwargs
    ):
        """
        :param roll: the roll object representing the equal working rolls of the pass
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (equal upper and lower)."""

        self.__dict__.update(kwargs)
        self._log = logging.getLogger(__name__)

    def local_height(self, z: float) -> float:
        coords = np.array([(1, -1), (1, 1)]) * (z, self.height)

        vline = LineString(
            coords
        )

        poly = Polygon(
            np.concatenate(
                [
                    self.upper_contour_line.coords,
                    self.lower_contour_line.coords
                ]
            )
        )

        intersection = vline.intersection(poly)

        return intersection.length

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

    @property
    def disk_elements(self) -> List['RollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    def init_solve(self, in_profile: BaseProfile):
        super().init_solve(in_profile)

        rotator = Rotator(rotation=self.in_profile_rotation, duration=0, length=0)
        rotator.solve(in_profile)

        self.in_profile = self.InProfile(self, rotator.out_profile)
        self.out_profile = self.OutProfile(self, rotator.out_profile)

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results], axis=0)

    def clear_hook_cache(self):
        super().clear_hook_cache()
        self.roll.clear_hook_cache()

    class Profile(DiskedUnit.Profile, DeformationUnit.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(RollPass, self.unit)

    class InProfile(Profile, DiskedUnit.InProfile, DeformationUnit.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, DiskedUnit.OutProfile, DeformationUnit.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()

    class Roll(BaseRoll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        def __init__(self, template: BaseRoll, roll_pass: 'RollPass'):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_")
            )
            super().__init__(**kwargs)

            self._roll_pass = weakref.ref(roll_pass)

        @property
        def roll_pass(self):
            """Reference to the roll pass this roll is used in."""
            return self._roll_pass()

    class DiskElement(DiskedUnit.DiskElement, DeformationUnit):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(RollPass, self.parent)

        class Profile(DiskedUnit.DiskElement.Profile, DeformationUnit.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'RollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(RollPass.DiskElement, self.unit)

        class InProfile(Profile, DiskedUnit.DiskElement.InProfile, DeformationUnit.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, DiskedUnit.DiskElement.OutProfile, DeformationUnit.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
