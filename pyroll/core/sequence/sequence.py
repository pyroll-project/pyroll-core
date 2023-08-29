from collections.abc import Sequence
from typing import overload, List, cast

from ..unit import Unit
from ..hooks import Hook


class PassSequence(Unit, Sequence[Unit]):
    """
    Represents a sequence of other units.
    Main container for defining rolling processes.
    Can be nested to define distinct rolling lines or similar.
    """

    elongation = Hook[float]()
    """Coefficient of elongation (change in length)."""

    log_elongation = Hook[float]()
    """Log. coefficient of elongation (change in length)."""

    abs_elongation = Hook[float]()
    """Absolute elongation (change in length)."""

    rel_elongation = Hook[float]()
    """Relative elongation (change in length)."""

    def __init__(self, units: Sequence[Unit], label: str = "", **kwargs):
        """
        :param units: sequence of unit objects
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label=label)
        self.__dict__.update(kwargs)
        self._subunits = self._SubUnitsList(self, units)

    class Profile(Unit.Profile):
        """Represents a profile in context of a pass sequence unit."""

        @property
        def pass_sequence(self) -> 'PassSequence':
            """Reference to the pass sequence. Alias for ``self.unit``."""
            return cast(PassSequence, self.unit)

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a pass sequence unit."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a pass sequence unit."""

        def root_hook_fallback(self, hook):
            """Copy the value from the in profile as fallback for root hooks."""
            return getattr(self.unit.units[-1].out_profile, hook.name, None)

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

    @property
    def __attrs__(self):
        return super().__attrs__ | {
            "units": self.units
        }
