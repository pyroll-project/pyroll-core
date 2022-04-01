import logging

import numpy as np

from pyroll.core.profile import Profile
from pyroll.core.unit import Unit
from pyroll.utils.plugin_host import PluginHost


class Transport(Unit, metaclass=PluginHost):
    hooks = set()

    def __init__(
            self,
            time: float,
            label: str = "",
            **kwargs
    ):
        super().__init__(label)
        self.time = time

        self.__dict__.update(kwargs)

        self._log = logging.getLogger(__name__)

        self.hook_args = dict(
            transport=self
        )

    def __str__(self):
        return "Transport {label} for {time:.4g}".format(
            label=f"'{self.label}' " if self.label else "",
            time=self.time
        )

    def solve(self, in_profile):
        self.in_profile = in_profile

        self._log.info(f"Starting transport of profile with temperature: {self.in_profile.temperature:.2f}K")

        self.in_profile = TransportInProfile(self, in_profile)
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


class TransportProfile(Profile, metaclass=PluginHost):
    def __init__(self, transport: Transport, **kwargs):
        super().__init__(**kwargs)
        self.hook_args = dict(
            profile=self,
            transport=transport
        )


class TransportInProfile(TransportProfile, metaclass=PluginHost):
    def __init__(self, transport: Transport, template: Profile):
        kwargs = template.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        super().__init__(transport, **kwargs)


class TransportOutProfile(TransportProfile, metaclass=PluginHost):
    hooks = set()

    def __init__(self, transport: Transport):
        kwargs = transport.in_profile.__dict__.copy()
        kwargs = dict([item for item in kwargs.items() if not item[0].startswith("_")])
        super().__init__(transport, **kwargs)
