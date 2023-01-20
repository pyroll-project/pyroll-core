import logging
from typing import List, cast

from .transport import Transport
from ..hooks import Hook


class Furnace(Transport):
    """Represents a furnace. Specialized version of a transport."""

    atmosphere_composition = Hook[dict[str, float]]()
    """Chemical composition of the furnace atmosphere. Dictionary of strings identifying the species mapped to floats representing their concentration."""

    wall_surface_area = Hook[float]()
    """Surface area of the inner wall surface (f.e. for radiation of the inner wall)."""

    wall_surface_perimeter = Hook[float]()
    """
    Perimeter of the inner wall surface (surface area per unit length).
    Replacement for ``wall_surface_area`` if the length scale is undefined.
    """

    wall_temperature = Hook[float]()
    """Temperature of the inner wall (f.e. for radiation of the inner wall)."""



    def __init__(
            self,
            label: str = "",
            **kwargs
    ):
        """
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label)
        self.__dict__.update(kwargs)
        self._log = logging.getLogger(__name__)

    @property
    def disk_elements(self) -> List['Furnace.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(Transport.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def furnace(self) -> 'Furnace':
            return cast(Furnace, self.unit)

    class InProfile(Profile, Transport.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, Transport.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(Transport.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def furnace(self) -> 'Furnace':
            return cast(Furnace, self.parent)

        class Profile(Transport.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

        class InProfile(Profile, Transport.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, Transport.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
