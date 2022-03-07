import logging

import numpy as np
import pluggy

from pyroll.core.profile import Profile
from pyroll.core.unit import Unit


class Transport(Unit):
    plugin_manager = pluggy.PluginManager("pyroll_transport")
    hookspec = pluggy.HookspecMarker("pyroll_transport")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_transport")

    hooks = set()

    _hook_results_to_clear = set()

    def __init__(
            self,
            time: float,
            environment_temperature: float = 293,
            label: str = "Transport",
            **kwargs
    ):
        super().__init__(label)
        self.time = time
        self.environment_temperature = environment_temperature

        self.__dict__.update(kwargs)

        self._log = logging.getLogger(__name__)

    def __getattr__(self, key):
        if hasattr(Transport.plugin_manager.hook, key):
            return self.get_from_hook(key)
        return super().__getattr__(key)

    def get_from_hook(self, key):
        if not hasattr(Transport.plugin_manager.hook, key):
            return super().get_from_hook(key)

        hook = getattr(Transport.plugin_manager.hook, key)
        result = hook(transport=self)

        if result is None:
            return None

        self.__dict__[key] = result
        Transport._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in Transport._hook_results_to_clear:
            if key in self.__dict__:
                delattr(self, key)
        super().clear_hook_results()

    def solve(self, in_profile):
        self.in_profile = in_profile

        self._log.info(f"Starting transport of profile with temperature: {self.in_profile.temperature:.2f}K")

        self.in_profile = TransportInProfile(in_profile, self)
        self.out_profile = TransportOutProfile(self)

        old_values = np.full(len(self.hooks) + len(self.out_profile.hooks), np.nan)

        while True:
            self.clear_hook_results()
            self.out_profile.clear_hook_results()

            for key in self.hooks:
                self.get_from_hook(key)

            for key in self.out_profile.hooks:
                self.out_profile.get_from_hook(key)

            current_values = np.array(
                list(map(lambda h: getattr(self, h), self.hooks))
                +
                list(map(lambda h: getattr(self.out_profile, h), self.out_profile.hooks))
            )
            if np.all((current_values - old_values) <= old_values * 1e-2):
                break

            old_values = current_values

        return self.out_profile


class TransportProfile(Profile):
    plugin_manager = pluggy.PluginManager("pyroll_transport_profile")
    hookspec = pluggy.HookspecMarker("pyroll_transport_profile")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_transport_profile")

    _hook_results_to_clear = set()

    def __getattr__(self, key):
        if hasattr(TransportProfile.plugin_manager.hook, key):
            return self.get_from_hook(key)
        return super().__getattr__(key)

    def get_from_hook(self, key):
        if not hasattr(TransportProfile.plugin_manager.hook, key):
            return super().get_from_hook(key)
        hook = getattr(TransportProfile.plugin_manager.hook, key)
        result = hook(transport=self._transport, profile=self)

        if result is None:
            return None

        self.__dict__[key] = result
        TransportProfile._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in TransportProfile._hook_results_to_clear:
            if key in self.__dict__:
                delattr(self, key)
        super().clear_hook_results()


class TransportInProfile(TransportProfile):
    def __init__(self, template: Profile, transport: Transport):
        kwargs = template.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        super().__init__(**kwargs)
        self._transport = transport


class TransportOutProfile(TransportProfile):
    plugin_manager = pluggy.PluginManager("pyroll_transport_out_profile")
    hookspec = pluggy.HookspecMarker("pyroll_transport_out_profile")(firstresult=True)
    hookimpl = pluggy.HookimplMarker("pyroll_transport_out_profile")

    hooks = set()

    _hook_results_to_clear = set()

    def __init__(self, transport: Transport):
        kwargs = transport.in_profile.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        super().__init__(**kwargs)
        self._transport = transport

    def __getattr__(self, key):
        if key in self.hooks:
            return getattr(self._transport.in_profile, key)
        if hasattr(TransportOutProfile.plugin_manager.hook, key):
            return self.get_from_hook(key)
        return super().__getattr__(key)

    def get_from_hook(self, key):
        if not hasattr(TransportOutProfile.plugin_manager.hook, key):
            return super().get_from_hook(key)
        hook = getattr(TransportOutProfile.plugin_manager.hook, key)
        result = hook(transport=self._transport, profile=self)

        if result is None:
            return None

        self.__dict__[key] = result
        TransportOutProfile._hook_results_to_clear.add(key)
        return self.__dict__[key]

    def clear_hook_results(self):
        for key in TransportOutProfile._hook_results_to_clear:
            if key in self.__dict__ and key not in self.hooks:
                delattr(self, key)
        super().clear_hook_results()
