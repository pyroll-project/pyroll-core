import logging
import weakref
from collections.abc import Sequence
from typing import overload, List

from ..unit import Unit
from ..profile import Profile as BaseProfile
from ..hooks import Hook


class PassSequence(Unit, Sequence[Unit]):
    """
    Represents a sequence of other units.
    Main container for defining rolling processes.
    Can be nested to define distinct rolling lines or similar.
    """

    total_elongation = Hook[float]()
    """Total elongation of the workpiece within the sequence."""

    def __init__(self, units: Sequence[Unit], label: str = "", **kwargs):
        """
        :param units: sequence of unit objects
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label=label)
        self.__dict__.update(kwargs)
        self._subunits = self._SubUnitsList(self, units)
        self._log = logging.getLogger(__name__)

    class Profile(Unit.Profile):
        """Represents a profile in context of a pass sequence unit."""

        def __init__(self, pass_sequence: 'PassSequence', template: BaseProfile):
            super().__init__(pass_sequence, template)
            self.pass_sequence = weakref.ref(pass_sequence)

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a pass sequence unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a pass sequence unit."""

    def __len__(self) -> int:
        return self._subunits.__len__()

    def __iter__(self):
        return self._subunits.__iter__()

    @overload
    def __getitem__(self, index: int) -> Unit:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[Unit]:
        ...

    def __getitem__(self, index: int) -> Unit:
        return self._subunits.__getitem__(index)

    @property
    def units(self) -> List[Unit]:
        return self._subunits
