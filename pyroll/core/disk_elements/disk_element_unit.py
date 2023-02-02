from typing import List, cast

from ..unit import Unit
from ..hooks import Hook
from ..profile import Profile as BaseProfile


class DiskElementUnit(Unit):
    """Base class for units that can be divided in disk elements."""

    disk_element_count = Hook[int]()
    """Number of intermediate profiles to create during unit solution (in and out profiles are not counted within)."""

    class Profile(Unit.Profile):
        """Represents a profile in context of a disked unit."""

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a disked unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a disked unit."""

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

            super().__init__(label=f"{parent}[{index}]", parent=parent, **kwargs)

        class Profile(Unit.Profile):
            """Represents a profile in context of a disk element unit."""

            @property
            def disk_element(self) -> 'DiskElementUnit.DiskElement':
                """Reference to the disk element. Alias for ``self.unit``"""
                return cast(DiskElementUnit.DiskElement, self.unit)

        class InProfile(Profile, Unit.InProfile):
            """Represents an incoming profile of a disk element unit."""

        class OutProfile(Profile, Unit.OutProfile):
            """Represents an outgoing profile of a disk element unit."""

    @property
    def disk_elements(self) -> List['DiskElement']:
        """A list of disk elements used to subdivide this unit."""
        return self._subunits

    @property
    def __attrs__(self):
        return super().__attrs__ | {
            "disk_elements": self.disk_elements
        }

    def init_solve(self, in_profile: BaseProfile):
        super().init_solve(in_profile)
        if not self._subunits:
            self._subunits = self._SubUnitsList(
                self, [self.DiskElement(self, i) for i in range(self.disk_element_count)]
                )
