import logging
import weakref
from collections.abc import Sequence
from typing import overload

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
        self.units = self.UnitsList(units)
        self._log = logging.getLogger(__name__)

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)

    def solve(self, in_profile: BaseProfile) -> BaseProfile:
        """
        Solve the workpiece evolution within this sequence by solving all units consecutively.

        :param in_profile: The incoming state profile
        :return: The outgoing state profile.
        """
        self._log.info(f"Started solving of {self}.")
        self.init_solve(in_profile)

        last_profile = in_profile
        for u in self.units:
            try:
                last_profile = u.solve(last_profile)
            except Exception as e:
                raise RuntimeError(f"Solution of pass sequence failed at unit {u}.") from e

        self.out_profile = self.OutProfile(self, self.units[-1].out_profile)

        return self.out_profile

    class Profile(Unit.Profile):
        """Represents a profile in context of a pass sequence unit."""

        def __init__(self, pass_sequence: 'PassSequence', template: BaseProfile):
            super().__init__(pass_sequence, template)
            self.pass_sequence = weakref.ref(pass_sequence)

    class InProfile(Profile):
        """Represents an incoming profile of a pass sequence unit."""

        def __init__(self, pass_sequence: 'PassSequence', template: BaseProfile):
            super().__init__(pass_sequence, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a pass sequence unit."""

        def __init__(self, pass_sequence: 'PassSequence', template: BaseProfile):
            super().__init__(pass_sequence, template)

    def __len__(self) -> int:
        return self.units.__len__()

    def __iter__(self):
        return self.units.__iter__()

    @overload
    def __getitem__(self, index: int) -> Unit:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[Unit]:
        ...

    def __getitem__(self, index: int) -> Unit:
        return self.units.__getitem__(index)

    class UnitsList(list):
        """Specialized list for holding the units of a pass sequence."""
        # noinspection PyProtectedMember
        def _repr_html_(self):
            return "<br/>".join(v._repr_html_() for v in self)


PassSequence.root_hooks = {
    PassSequence.total_elongation
}
