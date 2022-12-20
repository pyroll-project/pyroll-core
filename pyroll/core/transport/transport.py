import logging
import weakref

from ..hooks import Hook
from ..profile import Profile as BaseProfile
from ..unit import Unit


class Transport(Unit):
    """Represents a transport unit, e.g. an inter-rolling-stand gap, a furnace or cooling range."""

    duration = Hook[float]()
    """Time needed to pass the transport."""

    length = Hook[float]()
    """Spacial length of the transport."""

    velocity = Hook[float]()
    """Mean velocity of material flow."""

    environment_temperature = Hook[float]()
    """Temperature of the surrounding atmosphere."""

    def __init__(
            self,
            label: str = "",
            **kwargs
    ):
        """
        :param label: label for human identification
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """

        super().__init__(label)
        self.__dict__.update(kwargs)
        self._log = logging.getLogger(__name__)

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)
        self.out_profile = self.OutProfile(self)

    class Profile(Unit.Profile):
        """Represents a profile in context of a transport unit."""

        def __init__(self, transport: 'Transport', template: BaseProfile):
            super().__init__(transport, template)
            self.transport = weakref.ref(transport)

    class InProfile(Profile):
        """Represents an incoming profile of a transport unit."""

        def __init__(self, transport: 'Transport', template: BaseProfile):
            super().__init__(transport, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a transport unit."""

        def __init__(self, transport: 'Transport'):
            super().__init__(transport, transport.in_profile)


Transport.root_hooks = {
    Transport.OutProfile.strain,
}
