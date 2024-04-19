import copy
import weakref
from typing import Optional, Sequence, List, Iterable, SupportsIndex, Union, Callable

import numpy as np

from ..hooks import HookHost, Hook
from ..profile import Profile as BaseProfile
from timeit import default_timer as timer


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

    volume_flux = Hook[float]()
    """Flux/throughput of volume through this unit."""

    mass_flux = Hook[float]()
    """Flux/throughput of mass through this unit."""

    power = Hook[float]()
    """Total energy demand per time of this unit."""

    energy_consumption = Hook[float]()
    """Energy consumption of this unit per produced mass."""

    def __init__(self, label: str = "", parent=None, **kwargs):
        super().__init__()
        self.label = label
        """Label for human identification."""

        self._subunits: Optional[Unit._SubUnitsList] = self._SubUnitsList(self, [])

        self._parent = weakref.ref(parent) if parent is not None else None

        self.in_profile: Optional[Unit.InProfile] = None
        """The state of the incoming profile."""

        self.out_profile: Optional[Unit.OutProfile] = None
        """The state of the outgoing profile."""

        self.__dict__.update(kwargs)

        self._old_results = np.nan

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
        if i == 0:
            raise IndexError("This unit has no previous, as it is the first one.")
        return self.parent.subunits[i - 1]

    def prev_of(self, unit_type: type):
        """
        Returns the instance of the first predecessor of the given type in the sequence.
        Like the :py:attr:`Unit.prev` property, but returns the first unit with given type.

        :raises ValueError: if this unit has no parent unit
        """
        prev = self.prev

        while True:
            if isinstance(prev, unit_type):
                return prev
            prev = prev.prev

    @property
    def next(self):
        """
        Returns a reference to the successor of this unit in the sequence.

        :raises ValueError: if this unit has no parent unit
        """
        if self.parent is None:
            raise ValueError("This unit has no parent.")
        i = self.parent.subunits.index(self)
        if i == len(self.parent.subunits) - 1:
            raise IndexError("This unit has no next, as it is the last one.")
        return self.parent.subunits[i + 1]

    def next_of(self, unit_type: type):
        """
        Returns the instance of the first predecessor of the given type in the sequence.
        Like the :py:attr:`Unit.prev` property, but returns the first unit with given type.

        :raises ValueError: if this unit has no parent unit
        """
        next_ = self.next

        while True:
            if isinstance(next_, unit_type):
                return next_
            next_ = next_.next

    def init_solve(self, in_profile: BaseProfile):
        """
        Method called by the standard :py:meth:`solve` implementation to init
        the specialized profile instances for in and out.

        :param in_profile: the incoming state passed to :py:meth:`solve`
        """
        self.in_profile = self.InProfile(self, in_profile)
        if not self.out_profile:
            self.out_profile = self.OutProfile(self, in_profile)

    additional_inits: List[Callable] = []
    """A list of additional init methods for solution procedure which are directly called after init_solve. 
    Callables shall only take one parameter which is the unit instance (self)."""

    def __init_subclass__(cls, **kwargs):
        cls.additional_inits = []

    def _execute_additional_inits(self):
        for s in reversed(type(self).__mro__):
            inits = getattr(s, "additional_inits", None)

            if inits is not None:
                for init in inits:
                    init(self)

    def get_root_hook_results(self):
        in_profile_results = self.in_profile.evaluate_and_set_hooks()
        out_profile_results = self.out_profile.evaluate_and_set_hooks()
        self_results = self.evaluate_and_set_hooks()

        return np.concatenate([in_profile_results, self_results, out_profile_results], axis=0)

    def _solve_subunits(self):
        if self._subunits:
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
        start = timer()
        self.init_solve(in_profile)
        self._execute_additional_inits()

        for i in range(1, self.max_iteration_count):
            self.in_profile.reevaluate_cache()
            self._solve_subunits()
            self.reevaluate_cache()
            self.out_profile.reevaluate_cache()
            current_results = self.get_root_hook_results()

            if np.all(
                    np.abs(current_results - self._old_results)
                    <= np.abs(self._old_results) * self.iteration_precision
            ):
                self.logger.info(f"Finished solving of {self} after {i} iterations.")
                break

            self._old_results = current_results

        else:
            self.logger.warning(
                f"Solution iteration of {self} exceeded the maximum iteration count of {self.max_iteration_count}."
                f" Continuing anyway."
            )

        end = timer()
        self.logger.info(f"Solution took {end - start:.3f} s.")

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

    @property
    def profiles(self) -> List[BaseProfile]:
        """Returns a list of all profiles appearing in this unit.
        The list contains in and out profiles of all subunits and this unit itself in the order of rolling direction.
        This property recurses into all subunits."""

        def _yield_profiles():
            yield self.in_profile
            for u in self._subunits:
                yield from u.profiles
            yield self.out_profile

        return list(_yield_profiles())

    class Profile(BaseProfile):
        """Represents a profile in context of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_")
            )
            self._unit = weakref.ref(unit)
            super().__init__(**kwargs)

        @property
        def unit(self) -> 'Unit':
            """Reference to the parent unit, if applicable, else None."""
            return self._unit()

    class InProfile(Profile):
        """Represents an incoming profile of a unit."""

    class OutProfile(Profile):
        """Represents an outgoing profile of a unit."""

        def root_hook_fallback(self, hook):
            """Copy the value from the in profile as fallback for root hooks."""
            if self.unit.subunits:
                return getattr(self.unit.subunits[-1].out_profile, hook.name, None)
            return getattr(self.unit.in_profile, hook.name, None)

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

        def __deepcopy__(self, memo):
            cls = self.__class__
            result = cls.__new__(cls)

            o = self._owner()
            if id(o) in memo:
                result._owner = weakref.ref(memo[id(o)])
            else:
                result._owner = weakref.ref(copy.deepcopy(o, memo))

            for e in self:
                result.append(copy.deepcopy(e, memo))

            return result
