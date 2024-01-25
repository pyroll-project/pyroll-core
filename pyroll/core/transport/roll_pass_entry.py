from typing import List, cast

from .. import Transport
from ..hooks import Hook
from ..disk_elements import DiskElementUnit

class RollPassEntry(Transport):
    """Represents a roll pass entry side, derived from Transport."""

    environment_temperature = Hook[float]()
    """Temperature of the surrounding atmosphere."""



    @property
    def disk_elements(self) -> List['RollPassEntry.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a roll pass entry unit."""

        @property
        def roll_pass_entry(self) -> 'RollPassEntry':
            """Reference to the roll pass entry. Alias for ``self.unit``."""
            return cast(RollPassEntry, self.unit)

    class InProfile(Profile, DiskElementUnit.InProfile):
        """Represents an incoming profile of a roll pass entry unit."""

    class OutProfile(Profile, DiskElementUnit.OutProfile):
        """Represents an outgoing profile of a roll pass entry unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass entry."""

        @property
        def roll_pass_entry(self) -> 'RollPassEntry':
            """Reference to the roll pass entry. Alias for ``self.parent``."""
            return cast(RollPassEntry, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit within a roll pass entry."""

            @property
            def disk_element(self) -> 'RollPassEntry.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(RollPassEntry.DiskElement, self.unit)

            @property
            def roll_pass_entry(self) -> 'RollPassEntry':
                """Reference to the roll pass entry. Alias for ``self.unit.parent``"""
                return cast(RollPassEntry, self.unit.parent)

        class InProfile(Profile, DiskElementUnit.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit within a roll pass entry."""

        class OutProfile(Profile, DiskElementUnit.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit within a roll pass entry."""
