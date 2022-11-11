import logging
import weakref
from abc import abstractmethod
from typing import Optional, Set, List

import numpy as np

from ..exceptions import MaxIterationCountExceededError
from ..hooks import HookHost, Hook
from ..profile import Profile as BaseProfile


class Unit(HookHost):
    """Base class for units in a pass sequence."""

    profiles = Hook[List[BaseProfile]]()
    """List of all profile states within the unit."""

    in_profile = Hook[BaseProfile]()
    """The state of the incoming profile."""

    out_profile = Hook[BaseProfile]()
    """The state of the outgoing profile."""

    label = Hook[str]()
    """Label for human identification."""

    max_iteration_count = 100
    """Count of maximum solution loop iterations before aborting."""

    iteration_precision = 1e-2
    """Precision of iteration break in solution loop."""

    root_hooks: Set[Hook] = set()

    def __init__(self):
        super().__init__()
        self._log = logging.getLogger(__name__)

    def __str__(self):
        try:
            return type(self).__qualname__ + f" '{self.label}'"
        except (AttributeError, RecursionError):
            return type(self).__qualname__

    @abstractmethod
    def init_solve(self, in_profile: BaseProfile):
        """
        Method called by the standard :py:meth:`solve` implementation to init
        the specialized profile instances for in and out.

        :param in_profile: the incoming state passed to :py:meth:`solve`
        """
        raise NotImplementedError

    def get_root_hook_results(self):
        in_profile_results = self.in_profile.evaluate_and_set_hooks(self.root_hooks)
        self_results = self.evaluate_and_set_hooks(self.root_hooks)
        out_profile_results = self.out_profile.evaluate_and_set_hooks(self.root_hooks)

        return np.concatenate([in_profile_results, self_results, out_profile_results], axis=0)

    def clear_hook_cache(self):
        self.in_profile.clear_hook_cache()
        super().clear_hook_cache()
        self.out_profile.clear_hook_cache()

    def solve(self, in_profile: BaseProfile) -> BaseProfile:
        """
        Solve the workpiece evolution within this unit based on the incoming state specified by in_profile.
        Iterates several times calling :py:meth:`evaluate` until the return of :py:meth:`evaluate` does not change anymore.

        :param in_profile: The incoming state profile
        :return: The outgoing state profile.
        """
        self._log.info(f"Started solving of {self}.")
        self.init_solve(in_profile)
        old_values = np.nan

        for i in range(1, self.max_iteration_count):
            self.clear_hook_cache()
            current_values = self.get_root_hook_results()

            if np.all(np.abs(current_values - old_values) <= np.abs(old_values) * self.iteration_precision):
                self._log.info(f"Finished solving of {self} after {i} iterations.")

                result = BaseProfile(**{
                    k: v for k, v in self.out_profile.__dict__.items()
                    if not k.startswith("_")
                })
                return result

            old_values = current_values

        raise MaxIterationCountExceededError

    class Profile(BaseProfile):
        """Represents a profile in context of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_")
            )
            super().__init__(**kwargs)
            self.unit = weakref.ref(unit)

    class InProfile(Profile):
        """Represents an incoming profile of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            super().__init__(unit, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a unit."""

        def __init__(self, unit: 'Unit'):
            super().__init__(unit, unit.in_profile)
