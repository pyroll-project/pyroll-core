import logging
import weakref
from abc import abstractmethod
from typing import Set, List

import numpy as np

from ..hooks import HookHost, Hook
from ..profile import Profile as BaseProfile


class Unit(HookHost):
    """Base class for units."""

    profiles = Hook[List[BaseProfile]]()
    """List of all profile states within the unit."""

    in_profile = Hook[BaseProfile]()
    """The state of the incoming profile."""

    out_profile = Hook[BaseProfile]()
    """The state of the outgoing profile."""

    max_iteration_count = 100
    """Count of maximum solution loop iterations before aborting."""

    iteration_precision = 1e-2
    """Precision of iteration break in solution loop."""

    root_hooks: Set[Hook] = set()
    """
    Set of hooks to call explicitly in each solution iteration.
    Their values will be treated as explicitly set but reevaluated in every iteration.
    They will not be deleted during cache clearing.
    They serve as root for the calling tree and persistent iterational variables.
    """

    def __init__(self, label: str):
        super().__init__()
        self._log = logging.getLogger(__name__)
        self.label = label
        """Label for human identification."""

    def __str__(self):
        if self.label:
            return type(self).__qualname__ + f" '{self.label}'"
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
                break

            old_values = current_values

        else:
            self._log.warning(
                f"Solution iteration of {self} exceeded the maximum iteration count of {self.max_iteration_count}."
                f" Continuing anyway.")

        result = BaseProfile(**{
            k: v for k, v in self.out_profile.__dict__.items()
            if not k.startswith("_")
        })
        return result

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
