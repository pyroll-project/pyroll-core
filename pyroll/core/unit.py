from abc import ABC, abstractmethod
from typing import Optional

import pluggy

from .profile import Profile


class Unit(ABC):
    plugin_manager = pluggy.PluginManager("pyroll_unit")
    hookspec = pluggy.HookspecMarker("pyroll_unit")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_unit")

    hooks = set()

    _hook_results_to_clear = set()

    def __init__(self, label: str):
        self.out_profile: Optional[Profile] = None
        self.in_profile: Optional[Profile] = None
        self.label = label

    @abstractmethod
    def solve(self, in_profile: Profile) -> Profile:
        raise NotImplementedError

    def __getattr__(self, key):
        if hasattr(Unit.plugin_manager.hook, key):
            return self.get_from_hook(key)
        raise AttributeError(f"No attribute '{key}' or corresponding hook found!")

    def get_from_hook(self, key):
        hook = getattr(Unit.plugin_manager.hook, key)
        result = hook(unit=self)

        if result is None:
            return None

        self.__dict__[key] = result
        Unit._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in Unit._hook_results_to_clear:
            if key in self.__dict__:
                self.__dict__.pop(key, None)
