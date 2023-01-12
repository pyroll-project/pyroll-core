from typing import List

from ..unit import Unit
from ..hooks import Hook
from .disk_element import DiskElement as BaseDiskElement
from ..profile import Profile as BaseProfile


class DiskedUnit(Unit):
    """Base class for units that can be divided in disk elements."""

    disk_element_count = Hook[int]()
    """Number of intermediate profiles to create during unit solution (in and out profiles are not counted within)."""

    class Profile(Unit.Profile):
        """Represents a profile in context of a disked unit."""

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a disked unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a disked unit."""

    class DiskElement(BaseDiskElement):
        """Represents a disk element in a roll pass."""

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
        self._subunits = self._SubUnitsList(self, [self.DiskElement(self, i) for i in range(self.disk_element_count)])
