import weakref
from typing import List, Union, cast

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, Polygon

from ..disk_elements import DiskElementUnit
from ..hooks import Hook
from ..profile import Profile as BaseProfile
from ..roll import Roll as BaseRoll
from ..rotator import Rotator
from .deformation_unit import DeformationUnit


class RollPass(DiskElementUnit, DeformationUnit):
    """Represents a roll pass."""

    rotation = Hook[Union[bool, float]]()
    """
    Rotation applied to the incoming profile in ° (degree) before entry in this roll pass.
    Alternatively, provide a boolean value: false equals 0, 
    true means automatic determination from hook functions of ``Rotator.rotation``.
    """

    gap = Hook[float]()
    """Gap between the rolls (outer surface)."""

    height = Hook[float]()
    """Maximum height of the roll pass."""

    tip_width = Hook[float]()
    """Width of the intersection of the extended groove flanks (theoretical maximum filling width)."""

    roll_force = Hook[float]()
    """Vertical roll force."""

    mean_neutral_plane_position = Hook[float]()
    """Mean position of the neutral plane along the roll gap."""

    mean_neutral_plane_angle = Hook[float]()
    """Mean angle of the neutral plane along the roll gap."""

    mean_front_tension = Hook[float]()
    """Front tension acting on the current roll pass."""

    mean_back_tension = Hook[float]()
    """Back tension acting on the current roll pass."""

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

        super().__init__(label=label, **kwargs)

        self.roll = self.Roll(roll, self)
        """The working roll of this pass (equal upper and lower)."""

        self._contour_lines = None

    @property
    def contour_lines(self) -> List[LineString]:
        """List of line strings bounding the roll pass at the high point."""
        if self._contour_lines:
            return self._contour_lines

        upper = translate(self.roll.contour_line, yoff=self.gap / 2)
        lower = rotate(upper, angle=180, origin=(0, 0))

        self._contour_lines = [upper, lower]
        return self._contour_lines

    @property
    def types(self):
        """A tuple of keywords to specify the shape types of this roll pass.
        Shortcut to ``self.groove.types``."""
        return set(self.roll.groove.types)

    @property
    def disk_elements(self) -> List['RollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    def init_solve(self, in_profile: BaseProfile):
        if self.rotation:
            rotator = Rotator(
                # make True determining from hook functions
                rotation=self.rotation if self.rotation is not True else None,
                label=f"Auto-Rotator for {self}",
                duration=0, length=0, parent=self
            )
            rotator.solve(in_profile)
            in_profile = rotator.out_profile

        super().init_solve(in_profile)

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results], axis=0)

    def clear_cache(self):
        super().clear_cache()
        self.roll.clear_cache()
        self._contour_lines = None

    class Profile(DiskElementUnit.Profile, DeformationUnit.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(RollPass, self.unit)

    class InProfile(Profile, DiskElementUnit.InProfile, DeformationUnit.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, DiskElementUnit.OutProfile, DeformationUnit.OutProfile):
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

    class DiskElement(DiskElementUnit.DiskElement, DeformationUnit):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(RollPass, self.parent)

        class Profile(DiskElementUnit.DiskElement.Profile, DeformationUnit.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'RollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(RollPass.DiskElement, self.unit)

        class InProfile(Profile, DiskElementUnit.DiskElement.InProfile, DeformationUnit.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, DiskElementUnit.DiskElement.OutProfile, DeformationUnit.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
