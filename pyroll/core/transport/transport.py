import logging
import weakref
from typing import List

from ..hooks import Hook
from ..profile import Profile as BaseProfile
from ..disk_element import DiskedUnit


class Transport(DiskedUnit):
    """Represents a transport unit, e.g. an inter-rolling-stand gap, a furnace or cooling range."""

    environment_temperature = Hook[float]()
    """Temperature of the surrounding atmosphere."""

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
    def disk_elements(self) -> List['Transport.DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return list(self._subunits)

    class Profile(DiskedUnit.Profile):
        """Represents a profile in context of a transport unit."""

        def __init__(self, transport: 'Transport', template: BaseProfile):
            super().__init__(transport, template)
            self.transport = weakref.ref(transport)

    class InProfile(Profile, DiskedUnit.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, DiskedUnit.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(DiskedUnit.DiskElement):
        """Represents a disk element in a roll pass."""

        surface_area = Hook[float]()
        """Surface area of the disk element."""

        def transport(self) -> 'Transport':
            return self.parent()

        class Profile(DiskedUnit.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

        class InProfile(Profile, DiskedUnit.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, DiskedUnit.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
