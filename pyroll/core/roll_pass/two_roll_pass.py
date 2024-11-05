from typing import List, cast

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import LineString, MultiLineString

from .symmetric_roll_pass import SymmetricRollPass
from ..roll import Roll as BaseRoll


class TwoRollPass(SymmetricRollPass):
    """Represents a symmetric two-roll pass with equal upper and lower working roll."""

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

        upper = translate(self.roll.contour_line, yoff=self.gap / 2)
        lower = rotate(upper, angle=180, origin=(0, 0))

        self._contour_lines = MultiLineString([upper, lower])
        return self._contour_lines

    @property
    def disk_elements(self) -> List['TwoRollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    def get_root_hook_results(self):
        super_results = super().get_root_hook_results()
        roll_results = self.roll.evaluate_and_set_hooks()

        return np.concatenate([super_results, roll_results], axis=0)

    class Profile(SymmetricRollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'TwoRollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(TwoRollPass, self.unit)

    class InProfile(Profile, SymmetricRollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, SymmetricRollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

    class Roll(SymmetricRollPass.Roll):
        """Represents a roll applied in a :py:class:`TwoRollPass`."""

        @property
        def roll_pass(self) -> 'TwoRollPass':
            """Reference to the roll pass."""
            return cast(TwoRollPass, self._roll_pass())

    class DiskElement(SymmetricRollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'TwoRollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(TwoRollPass, self.parent)

        class Profile(SymmetricRollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'TwoRollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(TwoRollPass.DiskElement, self.unit)

        class InProfile(Profile, SymmetricRollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, SymmetricRollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
