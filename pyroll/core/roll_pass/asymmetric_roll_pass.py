from typing import List, cast

from shapely.affinity import translate, rotate
from shapely.geometry import LineString

from .base import BaseRollPass
from ..hooks import Hook
from ..roll import Roll as BaseRoll


class AsymmetricRollPass(BaseRollPass):
    """Represents a symmetric roll pass with equal upper and lower working roll."""

    def __init__(
            self,
            upper_roll: BaseRoll,
            lower_roll: BaseRoll,
            label: str = "",
            **kwargs
    ):
        super().__init__(label, **kwargs)

        self.upper_roll = self.Roll(upper_roll, self)
        """The upper working roll of this pass."""

        self.lower_roll = self.Roll(lower_roll, self)
        """The upper working roll of this pass."""


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
