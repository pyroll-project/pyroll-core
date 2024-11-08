from typing import List, cast

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, MultiLineString

from ..hooks import Hook
from .symmetric_roll_pass import SymmetricRollPass
from ..roll import Roll as BaseRoll


class ThreeRollPass(SymmetricRollPass):
    """Represents a roll pass with three working rolls and 3-fold symmetry."""

    inscribed_circle_diameter = Hook[float]()
    """Diameter of inscribed circle between roll barrels as alternative to roll gap definition."""

    def __init__(
            self,
            roll: BaseRoll,
            label: str = "",
            **kwargs
    ):
        super().__init__(roll, label, **kwargs)

    @property
    def contour_lines(self) -> MultiLineString:
        if self._contour_lines:
            return self._contour_lines

        shift = self.roll.groove.usable_width / 2 / np.sqrt(3) + self.gap / np.sqrt(3)
        lower = translate(self.roll.contour_line, yoff=shift)
        lower = LineString(lower.coords[::-1])  # get back coordinate order
        right = rotate(lower, angle=-60, origin=(0, 0))
        left = rotate(lower, angle=60, origin=(0, 0))
        lower = rotate(lower, angle=180, origin=(0, 0))

        self._contour_lines = MultiLineString([left, lower, right])
        return self._contour_lines

    @property
    def classifiers(self):
        """A tuple of keywords to specify the shape type classifiers of this roll pass.
        Shortcut to ``self.groove.classifiers``."""
        return set(self.roll.groove.classifiers) | {"3fold"}

    @property
    def disk_elements(self) -> List['ThreeRollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(SymmetricRollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'ThreeRollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(ThreeRollPass, self.unit)

    class InProfile(Profile, SymmetricRollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, SymmetricRollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()

    class Roll(SymmetricRollPass.Roll):
        """Represents a roll applied in a :py:class:`ThreeRollPass`."""

        @property
        def roll_pass(self) -> 'ThreeRollPass':
            """Reference to the roll pass."""
            return cast(ThreeRollPass, self._roll_pass())

    class DiskElement(SymmetricRollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'ThreeRollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(ThreeRollPass, self.parent)

        class Profile(SymmetricRollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'ThreeRollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(ThreeRollPass.DiskElement, self.unit)

        class InProfile(Profile, SymmetricRollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, SymmetricRollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
