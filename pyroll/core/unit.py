from typing import Optional, Set, Any, Dict

import numpy as np

from .plugin_host import PluginHost
from .profile import Profile as BaseProfile
from .exceptions import MaxIterationCountExceededError


class Unit(PluginHost):
    """Base class for units in a pass sequence."""

    max_iteration_count = 100
    """Count of maximum solution loop iterations before aborting."""

    iteration_precision = 1e-2
    """Precision of iteration break in solution loop."""

    def __init__(self, label: str):
        super().__init__(dict(unit=self))

        self.in_profile: Optional[BaseProfile] = None
        """Incoming workpiece state profile."""

        self.out_profile: Optional[BaseProfile] = None
        """Outgoing workpiece state profile."""

        self.label = label
        """Label for human identification."""

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
        in_profile_results = self.in_profile.get_root_hook_results()
        self_results = super().get_root_hook_results()
        out_profile_results = self.out_profile.get_root_hook_results()

        return np.concatenate([in_profile_results, self_results, out_profile_results], axis=0)

    def delete_hook_result_attributes(self):
        self.in_profile.delete_hook_result_attributes()
        super().delete_hook_result_attributes()
        self.out_profile.delete_hook_result_attributes()

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
            self.delete_hook_result_attributes()
            current_values = self.get_root_hook_results()

            if np.all(np.abs(current_values - old_values) <= np.abs(old_values) * self.iteration_precision):
                self._log.info(f"Finished solving of {self} after {i} iterations.")

                result = BaseProfile(**dict(
                    e for e in self.out_profile.__dict__.items()
                    if not e[0].startswith("_") and
                    (e[0] not in self.out_profile.hook_result_attributes or e[0] in self.out_profile.root_hooks)
                ))
                return result

            old_values = current_values

        raise MaxIterationCountExceededError

    class Profile(BaseProfile):
        """Represents a profile in context of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_") and
                (e[0] not in template.hook_result_attributes or e[0] in template.root_hooks)
            )
            super().__init__(**kwargs)
            self.hook_args["unit"] = unit

    class InProfile(Profile):
        """Represents an incoming profile of a unit."""

        def __init__(self, unit: 'Unit', template: BaseProfile):
            super().__init__(unit, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a unit."""

        def __init__(self, unit: 'Unit'):
            super().__init__(unit, unit.in_profile)

    def _repr_pretty_(self, p, cycle):
        return super()._repr_pretty_(p, cycle)
