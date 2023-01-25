import weakref
from typing import Optional, Sequence, List, Iterable, SupportsIndex, Union

import numpy as np

from ..hooks import HookHost, Hook
from ..profile import Profile as BaseProfile


class Unit(HookHost):
    """Base class for units."""

    max_iteration_count = Hook[int]()
    """Count of maximum solution loop iterations before aborting."""

    iteration_precision = Hook[float]()
    """Precision of iteration break in solution loop."""

    length = Hook[float]()
    """The length of the unit (spacial extent in rolling direction)."""

    duration = Hook[float]()
    """Time needed to pass the unit (temporal extent)."""

    velocity = Hook[float]()
    """Mean velocity of material flow."""

    volume = Hook[float]()
    """Volume of workpiece material within the unit."""

    surface_area = Hook[float]()
    """Surface area of workpiece within the unit."""

    def __init__(self, label: str, parent=None, **kwargs):
        super().__init__()
        self.label = label
        """Label for human identification."""

        self._subunits: Optional[Unit._SubUnitsList] = self._SubUnitsList(self, [])

        self._parent = weakref.ref(parent) if parent is not None else None

        self.in_profile = None
        """The state of the incoming profile."""

        self.out_profile = None
        """The state of the outgoing profile."""

        self.__dict__.update(kwargs)

    def __str__(self):
        if self.label:
            return type(self).__qualname__ + f" '{self.label}'"
        return type(self).__qualname__

    @property
    def prev(self):
        """
        Returns a reference to the predecessor of this unit in the sequence.

        :raises ValueError: if this unit has no parent unit
        """
        if self.parent is None:
            raise ValueError("This unit has no parent.")
        i = self.parent.subunits.index(self)
        return self.parent.subunits[i - 1]

    @property
    def next(self):
        """
        Returns a reference to the successor of this unit in the sequence.

        :raises ValueError: if this unit has no parent unit
        """
        if self.parent is None:
            raise ValueError("This unit has no parent.")
        i = self.parent.subunits.index(self)
        return self.parent.subunits[i + 1]

    def init_solve(self, in_profile: BaseProfile):
        """
        Method called by the standard :py:meth:`solve` implementation to init
        the specialized profile instances for in and out.

        :param in_profile: the incoming state passed to :py:meth:`solve`
        """
        self.in_profile = self.InProfile(self, in_profile)
        self.out_profile = self.OutProfile(self, in_profile)

    def get_root_hook_results(self):
        in_profile_results = self.in_profile.evaluate_and_set_hooks()
        self_results = self.evaluate_and_set_hooks()
        out_profile_results = self.out_profile.evaluate_and_set_hooks()

        return np.concatenate([in_profile_results, self_results, out_profile_results], axis=0)

    def clear_cache(self):
        self.in_profile.clear_cache()
        super().clear_cache()
        self.out_profile.clear_cache()

    def _solve_subunits(self):
        last_profile = self.in_profile
        for u in self._subunits:
            try:
                last_profile = u.solve(last_profile)
            except Exception as e:
                raise RuntimeError(f"Solution of sub units failed at unit {u}.") from e

    def solve(self, in_profile: BaseProfile) -> BaseProfile:
        """
        Solve the workpiece evolution within this unit based on the incoming state specified by in_profile.
        Iterates several times calling :py:meth:`evaluate` until the return of :py:meth:`evaluate` does not change anymore.

        :param in_profile: The incoming state profile
        :return: The outgoing state profile.
        """
        self.logger.info(f"Started solving of {self}.")
        self.init_solve(in_profile)
        old_values = np.nan

        for i in range(1, self.max_iteration_count):
            self.clear_cache()
            self._solve_subunits()
            current_values = self.get_root_hook_results()

            if np.all(np.abs(current_values - old_values) <= np.abs(old_values) * self.iteration_precision):
                self.logger.info(f"Finished solving of {self} after {i} iterations.")
                break

            old_values = current_values

        else:
            self.logger.warning(
                f"Solution iteration of {self} exceeded the maximum iteration count of {self.max_iteration_count}."
                f" Continuing anyway."
            )

        result = BaseProfile(
            **{
                k: v for k, v in self.out_profile.__dict__.items()
                if not k.startswith("_")
            }
        )
        return result

    @property
    def parent(self) -> Optional['Unit']:
        """Reference to the parent unit, if applicable, else None."""
        if self._parent is None:
            return None
        return self._parent()

    @parent.setter
    def parent(self, value: 'Unit'):
        """Sets Reference to the parent unit."""
        if value is None:
            self._parent = None
        else:
            self._parent = weakref.ref(value)

    @property
    def subunits(self) -> List['Unit']:
        """List of the subunits."""
        return self._subunits

    class Profile(BaseProfile):
        """Represents a profile in context of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_")
            )
            super().__init__(**kwargs)
            self._unit = weakref.ref(unit)

        @property
        def unit(self) -> 'Unit':
            """Reference to the parent unit, if applicable, else None."""
            return self._unit()

    class InProfile(Profile):
        """Represents an incoming profile of a unit."""

    class OutProfile(Profile):
        """Represents an outgoing profile of a unit."""

    class _SubUnitsList(list):
        """Specialized list for holding the units of a pass sequence."""

        def __init__(self, owner: 'Unit', units: Sequence['Unit']):
            super().__init__(units)
            self._owner = weakref.ref(owner)
            for u in self:
                u.parent = owner

        def append(self, unit: 'Unit') -> None:
            unit.parent = self._owner()
            super().append(unit)

        def extend(self, units: Iterable['Unit']) -> None:
            for u in units:
                u.parent = self._owner()
            super().extend(units)

        def insert(self, i: Union[SupportsIndex, slice], unit: 'Unit') -> None:
            unit.parent = self._owner()
            super().insert(i, unit)

        def pop(self, i: Union[SupportsIndex, slice] = ...) -> 'Unit':
            unit = super().pop(i)
            unit.parent = None
            return unit

        def clear(self) -> None:
            for u in self:
                u.parent = None
            super().clear()

        def copy(self) -> 'Unit._SubUnitsList':
            return self.__init__(self._owner(), self)

        def __setitem__(self, i: Union[SupportsIndex, slice], value: 'Unit'):
            current = self[i]
            if isinstance(current, list):
                for u in current:
                    u.parent = None
            else:
                current.parent = None
            return super().__setitem__(i, value)

        def __delitem__(self, i: Union[SupportsIndex, slice]):
            current = self[i]
            if isinstance(current, list):
                for u in current:
                    u.parent = None
            else:
                current.parent = None
            return super().__delitem__(i)

        # noinspection PyProtectedMember
        def _repr_html_(self):
            return "<br/>".join(v._repr_html_() for v in self)
