import logging
from ..grooves import GrooveBase
from ..plugin_host import PluginHost


class Roll(PluginHost):
    def __init__(
            self,
            groove: GrooveBase,
            **kwargs):
        self.__dict__.update(kwargs)

        super().__init__(dict(
            roll=self
        ))

        self.groove = groove
        self._log = logging.getLogger(__name__)
