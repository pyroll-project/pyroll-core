from typing import List, cast

from ..hooks import Hook
from .transport import Transport

__all__ = ["Shear"]


class Shear(Transport):
    """Represents a shear."""

    cut_length = Hook[float]()
    """Length of the material the shear cuts from the profile."""


    @property
    def disk_elements(self) -> List["CoolingPipe.DiskElement"]:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def shear(self) -> "Shear":
            """Reference to the shear. Alias for ``self.unit``."""
            return cast(Shear, self.unit)

    class InProfile(Profile, Transport.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, Transport.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def shear(self) -> "Shear":
            """Reference to the shear. Alias for ``self.parent``."""
            return cast(Shear, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> "Shear.DiskElement":
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(Shear.DiskElement, self.unit)

            @property
            def shear(self) -> "CoolingPipe":
                """Reference to the transport. Alias for ``self.unit.parent``"""
                return cast(Shear, self.unit.parent)

        class InProfile(Profile, Transport.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, Transport.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
