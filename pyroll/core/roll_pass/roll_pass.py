from typing import List, cast

from shapely.affinity import translate, rotate
from shapely.geometry import LineString

from .base import BaseRollPass
from ..hooks import Hook


class RollPass(BaseRollPass):
    """Represents a roll pass with three working rolls and 3-fold symmetry."""

    @property
    def contour_lines(self) -> List[LineString]:
        if self._contour_lines:
            return self._contour_lines

        upper = translate(self.roll.contour_line, yoff=self.gap / 2)
        lower = rotate(upper, angle=180, origin=(0, 0))

        self._contour_lines = [upper, lower]
        return self._contour_lines

    @property
    def disk_elements(self) -> List['RollPass.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(BaseRollPass.Profile):
        """Represents a profile in context of a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.unit``."""
            return cast(RollPass, self.unit)

    class InProfile(Profile, BaseRollPass.InProfile):
        """Represents an incoming profile of a roll pass."""

    class OutProfile(Profile, BaseRollPass.OutProfile):
        """Represents an outgoing profile of a roll pass."""

        filling_ratio = Hook[float]()

    class Roll(BaseRollPass.Roll):
        """Represents a roll applied in a :py:class:`RollPass`."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass."""
            return cast(RollPass, self._roll_pass())

    class DiskElement(BaseRollPass.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def roll_pass(self) -> 'RollPass':
            """Reference to the roll pass. Alias for ``self.parent``."""
            return cast(RollPass, self.parent)

        class Profile(BaseRollPass.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'RollPass.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(RollPass.DiskElement, self.unit)

        class InProfile(Profile, BaseRollPass.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, BaseRollPass.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
