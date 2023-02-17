from typing import List, cast

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString

from ..hooks import Hook
from ..roll_pass import RollPass
from ..roll import Roll as BaseRoll


class ThreeRollPass(RollPass):
    """Represents a roll pass with three working rolls and 3-fold symmetry."""

    @property
    def contour_lines(self) -> List[LineString]:
        if self._contour_lines:
            return self._contour_lines

        shift = self.roll.groove.usable_width / 2 / np.sqrt(3) + self.gap / np.sqrt(3)
        lower = rotate(translate(self.roll.contour_line, yoff=shift), angle=180, origin=(0, 0))
        lower = LineString(lower.coords[::-1])  # get back coordinate order
        right = rotate(lower, angle=120, origin=(0, 0))
        left = rotate(lower, angle=-120, origin=(0, 0))

        self._contour_lines = [left, lower, right]
        return self._contour_lines

    @property
    def classifiers(self):
        """A tuple of keywords to specify the shape type classifiers of this roll pass.
        Shortcut to ``self.groove.classifiers``."""
        return set(self.roll.groove.classifiers) | {"3fold"}

    @property
    def disk_elements(self) -> List['RollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(RollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(RollPass, self.unit)

    class InProfile(Profile, RollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, RollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()

    class Roll(RollPass.Roll):
        """Represents a roll applied in a :py:class:`ThreeRollPass`."""

        @property
        def roll_pass(self) -> 'ThreeRollPass':
            """Reference to the roll pass."""
            return cast(ThreeRollPass, self._roll_pass())

    class DiskElement(RollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'ThreeRollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(ThreeRollPass, self.parent)

        class Profile(RollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'ThreeRollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(ThreeRollPass.DiskElement, self.unit)

        class InProfile(Profile, RollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, RollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
