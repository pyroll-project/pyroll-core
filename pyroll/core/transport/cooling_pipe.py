from typing import List, cast

from ..hooks import Hook
from .transport import Transport


class CoolingPipe(Transport):
    """Represents a smooth cooling pipe."""

    inner_diameter = Hook[float]()
    """Inner diameter of the cooling pipe"""

    cooling_water_volume_flux = Hook[float]()
    """Volume flux of the cooling water"""

    cooling_water_temperature = Hook[float]()
    """Temperature of the cooling water"""


    @property
    def disk_elements(self) -> List['CoolingPipe.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def cooling_pipe(self) -> 'CoolingPipe':
            """Reference to the transport. Alias for ``self.unit``."""
            return cast(CoolingPipe, self.unit)

    class InProfile(Profile, Transport.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, Transport.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def cooling_pipe(self) -> 'CoolingPipe':
            """Reference to the transport. Alias for ``self.parent``."""
            return cast(CoolingPipe, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'CoolingPipe.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(CoolingPipe.DiskElement, self.unit)

            @property
            def cooling_pipe(self) -> 'CoolingPipe':
                """Reference to the transport. Alias for ``self.unit.parent``"""
                return cast(CoolingPipe, self.unit.parent)

        class InProfile(Profile, Transport.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, Transport.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
