from typing import List, cast

from ..hooks import Hook
from ..disk_elements import DiskElementUnit


class Transport(DiskElementUnit):
    """Represents a transport unit, e.g. an inter-rolling-stand gap, a furnace or cooling range."""

    environment_temperature = Hook[float]()
    """Temperature of the surrounding atmosphere."""

    @property
    def disk_elements(self) -> List['Transport.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(DiskElementUnit.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def transport(self) -> 'Transport':
            """Reference to the transport. Alias for ``self.unit``."""
            return cast(Transport, self.unit)

    class InProfile(Profile, DiskElementUnit.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, DiskElementUnit.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(DiskElementUnit.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def transport(self) -> 'Transport':
            """Reference to the transport. Alias for ``self.parent``."""
            return cast(Transport, self.parent)

        class Profile(DiskElementUnit.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'Transport.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(Transport.DiskElement, self.unit)

            @property
            def transport(self) -> 'Transport':
                """Reference to the transport. Alias for ``self.unit.parent``"""
                return cast(Transport, self.unit.parent)

        class InProfile(Profile, DiskElementUnit.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, DiskElementUnit.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
