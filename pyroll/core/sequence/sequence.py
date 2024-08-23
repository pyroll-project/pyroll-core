from collections.abc import Sequence
from typing import overload, List, cast

from ..unit import Unit
from ..roll_pass import RollPass
from ..transport import Transport
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

    def __len__(self) -> int:
        return self._subunits.__len__()

    def __iter__(self):
        return self._subunits.__iter__()

    @overload
    def __getitem__(self, key: int) -> Unit:
        """Gets unit item by index."""
        ...

    @overload
    def __getitem__(self, key: str) -> Unit:
        """Gets unit item by label."""
        ...

    @overload
    def __getitem__(self, key: slice) -> list[Unit]:
        """Gets a slice of units."""
        ...

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                return next(u for u in self._subunits if u.label == key)
            except StopIteration:
                raise KeyError(f"No unit with label '{key}' found.")

        if isinstance(key, int) or isinstance(key, slice):
            return self._subunits.__getitem__(key)

        raise TypeError("Key must be int, slice or str")

    def prepend(self, unit: Unit) -> None:
        """Prepend a unit to the beginning of the sequence."""
        self._subunits.insert(0, unit)

    def append(self, unit: Unit) -> None:
        """Append a unit to the end of the sequence."""
        self._subunits.append(unit)

    def drop(self, index: int) -> None:
        """Remove the unit at the specified index from the sequence."""
        del self._subunits[index]

    @property
    def units(self) -> List[Unit]:
        """Returns a list of all units in this sequence."""
        return list(self._subunits)

    @property
    def roll_passes(self) -> List[RollPass]:
        """Returns a list of all roll passes in this sequence."""
        return list(u for u in self._subunits if isinstance(u, RollPass))

    @property
    def transports(self) -> List[Transport]:
        """Returns a list of all transports in this sequence."""
        return list(u for u in self._subunits if isinstance(u, Transport))

    @property
    def __attrs__(self):
        return super().__attrs__ | {
            "units": self.units
        }

    def _ipython_key_completions_(self):
        return [u.label for u in self._subunits]
