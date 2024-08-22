from typing import cast

from ..hooks import Hook
from ..unit import Unit


class Rotator(Unit):
    """Represents a unit rotating a profile around the rolling axis (mostly for feeding into next roll pass)."""

    rotation = Hook[float]()
    """Rotation applied to the profile in ° (degree)."""

    @property
    def prev_roll_pass(self):
        """
        Returns a reference to the first preceding roll pass of this unit in the sequence.
        If the parent of this unit is a roll pass,
        it is considered as the next roll pass, so the preceding of this is searched.

        :raises ValueError: if this unit has no parent unit
        """
        from ..roll_pass.base import BaseRollPass

        if isinstance(self.parent, BaseRollPass):
            return self.parent.prev_of(BaseRollPass)

        return self.prev_of(BaseRollPass)

    @property
    def next_roll_pass(self):
        """
        Returns a reference to the first succeeding roll pass of this unit in the sequence.
        If the parent of this unit is a roll pass, it is considered as the next roll pass.

        :raises ValueError: if this unit has no parent unit
        """
        from ..roll_pass.base import BaseRollPass

        if isinstance(self.parent, BaseRollPass):
            return self.parent

        return self.next_of(BaseRollPass)

    class Profile(Unit.Profile):
        """Represents a profile in context of a rotator."""

        @property
        def rotator(self) -> 'Rotator':
            """Reference to the rotator. Alias for ``self.unit``."""
            return cast(Rotator, self.unit)

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a rotator."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a rotator."""
