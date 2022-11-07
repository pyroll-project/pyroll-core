import logging

from ..profile import Profile as BaseProfile
from ..unit import Unit


class Transport(Unit):
    """Represents a transport unit, e.g. an inter-rolling-stand gap, a furnace or cooling range."""

    root_hooks = {

    }

    def __init__(
            self,
            label: str = "",
            **kwargs
    ):
        super().__init__(label)

        self.__dict__.update(kwargs)

        self._log = logging.getLogger(__name__)

    def __str__(self):
        return "Transport {label}".format(
            label=f"'{self.label}' " if self.label else ""
        )

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)
        self.out_profile = self.OutProfile(self)

    class Profile(Unit.Profile):
        """Represents a profile in context of a transport unit."""

        def __init__(self, transport: 'Transport', template: BaseProfile):
            super().__init__(transport, template)
            self.transport = transport

    class InProfile(Profile):
        """Represents an incoming profile of a transport unit."""

        def __init__(self, transport: 'Transport', template: BaseProfile):
            super().__init__(transport, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a transport unit."""

        def __init__(self, transport: 'Transport'):
            super().__init__(transport, transport.in_profile)
