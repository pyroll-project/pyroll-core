import logging
import weakref

from ..hooks import Hook
from ..unit import Unit
from ..profile import Profile as BaseProfile


class Rotator(Unit):
    """Represents a unit rotating a profile around the rolling axis (mostly for feeding into next roll pass)."""

    rotation = Hook[float]()
    """Rotation applied to the profile in ° (degree)."""

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

    class Profile(Unit.Profile):
        """Represents a profile in context of a rotator."""

        def __init__(self, rotator: 'Rotator', template: BaseProfile):
            super().__init__(rotator, template)
            self.rotator = weakref.ref(rotator)

    class InProfile(Profile, Unit.InProfile):
        """Represents an incoming profile of a rotator."""

    class OutProfile(Profile, Unit.OutProfile):
        """Represents an outgoing profile of a rotator."""
