import logging
from typing import cast

from ..unit import Unit


class DiskElement(Unit):
    """
    Represents a disk element unit, a unit used to subdivide other units in rolling direction.
    The basic disk element is not intended to be used directly.
    Use the specialized disk elements of the respective parent unit instead.
    """

    def __init__(
            self,
            parent: 'Unit',
            index: int,
            **kwargs
    ):
        """
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label=f"{parent}[{index}]", parent=parent)
        self.__dict__.update(kwargs)
        self._log = logging.getLogger(__name__)

    @property
    def parent(self) -> 'Unit':
        """Reference to the roll pass. Alias for ``self.parent``."""
        return super().parent

    class Profile(Unit.Profile):
        """Represents a profile in context of a disk element unit."""

        @property
        def disk_element(self) -> 'DiskElement':
            """Reference to the disk element. Alias for ``self.unit``"""
            return cast(DiskElement, self.unit)

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a disk element unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a disk element unit."""
