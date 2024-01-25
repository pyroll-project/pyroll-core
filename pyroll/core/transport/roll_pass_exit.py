from typing import List, cast

from .. import Transport
from ..hooks import Hook
from ..disk_elements import DiskElementUnit

class RollPassExit(Transport):
    """Represents a roll pass exit side, derived from Transport."""

    environment_temperature = Hook[float]()
    """Temperature of the surrounding atmosphere."""

    cooling_water_temperature = Hook[float]()
    """Temperature of the cooling water used for the roll pass."""

    @property
    def disk_elements(self) -> List['RollPassExit.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a roll pass exit unit."""

        @property
        def roll_pass_exit(self) -> 'RollPassExit':
            """Reference to the roll pass exit. Alias for ``self.unit``."""
            return cast(RollPassExit, self.unit)

    class InProfile(Profile, DiskElementUnit.InProfile):
        """Represents an incoming profile of a roll pass exit unit."""

    class OutProfile(Profile, DiskElementUnit.OutProfile):
        """Represents an outgoing profile of a roll pass exit unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass exit."""

        @property
        def roll_pass_exit(self) -> 'RollPassExit':
            """Reference to the roll pass exit. Alias for ``self.parent``."""
            return cast(RollPassExit, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit within a roll pass exit."""

            @property
            def disk_element(self) -> 'RollPassExit.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(RollPassExit.DiskElement, self.unit)

            @property
            def roll_pass_exit(self) -> 'RollPassExit':
                """Reference to the roll pass exit. Alias for ``self.unit.parent``"""
                return cast(RollPassExit, self.unit.parent)

        class InProfile(Profile, DiskElementUnit.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit within a roll pass exit."""

        class OutProfile(Profile, DiskElementUnit.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit within a roll pass exit."""
