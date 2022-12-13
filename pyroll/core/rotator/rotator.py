import logging
import weakref

from ..hooks import Hook
from ..unit import Unit
from ..profile import Profile as BaseProfile


class Rotator(Unit):
    rotation = Hook[float]()

    def __init__(
            self,
            label: str = "",
            **kwargs
    ):
        super().__init__(label)
        self.__dict__.update(kwargs)
        self._log = logging.getLogger(__name__)

    def init_solve(self, in_profile: BaseProfile):
        self.in_profile = self.InProfile(self, in_profile)
        self.out_profile = self.OutProfile(self)

    class Profile(BaseProfile):
        """Represents a profile in context of a unit."""

        def __init__(self, rotator: 'Rotator', template: BaseProfile):
            kwargs = dict(
                e for e in template.__dict__.items()
                if not e[0].startswith("_")
            )
            super().__init__(**kwargs)
            self.rotator = weakref.ref(rotator)

    class InProfile(Profile):
        """Represents an incoming profile of a unit."""

        def __init__(self, rotator: 'Rotator', template: BaseProfile):
            super().__init__(rotator, template)

    class OutProfile(Profile):
        """Represents an outgoing profile of a unit."""

        def __init__(self, rotator: 'Rotator'):
            super().__init__(rotator, rotator.in_profile)


Rotator.root_hooks = {
    Rotator.OutProfile.cross_section,
}
