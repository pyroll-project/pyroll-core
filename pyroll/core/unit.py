import logging
from typing import Optional, Set, Any, Dict

import numpy as np

from .plugin_host import PluginHost, HookCaller, evaluate_and_pin_hooks
from .profile import Profile as BaseProfile
from .exceptions import MaxIterationCountExceededError


class Unit(PluginHost):
    """Base class for units in a pass sequence."""

    max_iteration_count = 100
    """Count of maximum solution loop iterations before aborting."""

    iteration_precision = 1e-2
    """Precision of iteration break in solution loop."""

    root_hooks: Set[HookCaller] = set()

    def __init__(self, label: str):
        super().__init__()

        self.in_profile: Optional[BaseProfile] = None
        """Incoming workpiece state profile."""

        self.out_profile: Optional[BaseProfile] = None
        """Outgoing workpiece state profile."""

        self.label = label
        """Label for human identification."""

        self._log = logging.getLogger(__name__)

    def __repr__(self):
        sep = ",\n\t"
        kwattrs = sorted(f"{name}={value}" for name, value in self.__dict__.items() if not name.startswith("_"))
        return f"{self.__class__.__name__}(\n\t{sep.join(kwattrs)}\n)"

    def init_solve(self, in_profile: BaseProfile):
        """
        Method called by the standard :py:meth:`solve` implementation to init
        the specialized profile instances for in and out.

        :param in_profile: the incoming state passed to :py:meth:`solve`
        """
        raise NotImplementedError

    def get_root_hook_results(self):
        in_profile_results = evaluate_and_pin_hooks(self.in_profile, self.root_hooks)
        self_results = evaluate_and_pin_hooks(self, self.root_hooks)
        out_profile_results = evaluate_and_pin_hooks(self.out_profile, self.root_hooks)

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

                result = BaseProfile(**dict(
                    e for e in self.out_profile.__dict__.items()
                    if not e[0].startswith("_")
                ))
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
            self.unit = unit

    class InProfile(Profile):
        """Represents an incoming profile of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            super().__init__(unit, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a unit."""

        def __init__(self, unit: 'Unit'):
            super().__init__(unit, unit.in_profile)
