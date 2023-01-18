import logging
from typing import List, cast

from ..hooks import Hook
from ..disk_elements import DiskedUnit


class Transport(DiskedUnit):
    """Represents a transport unit, e.g. an inter-rolling-stand gap, a furnace or cooling range."""

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
        return self._subunits

    class Profile(DiskedUnit.Profile):
        """Represents a profile in context of a transport unit."""

        @property
        def transport(self) -> 'Transport':
            """Reference to the transport. Alias for ``self.unit``."""
            return cast(Transport, self.unit)

    class InProfile(Profile, DiskedUnit.InProfile):
        """Represents an incoming profile of a transport unit."""

    class OutProfile(Profile, DiskedUnit.OutProfile):
        """Represents an outgoing profile of a transport unit."""

    class DiskElement(DiskedUnit.DiskElement):
        """Represents a disk element in a roll pass."""

        @property
        def transport(self) -> 'Transport':
            """Reference to the transport. Alias for ``self.parent``."""
            return cast(Transport, self.parent)

        class Profile(DiskedUnit.DiskElement.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'Transport.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(Transport.DiskElement, self.unit)

        class InProfile(Profile, DiskedUnit.DiskElement.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, DiskedUnit.DiskElement.OutProfile):
            """Represents an outgoing profile of a disk element unit."""
