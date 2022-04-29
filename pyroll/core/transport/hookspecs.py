import sys

from .transport import Transport


@Transport.OutProfile.hookspec
def strain(transport):
    """The equivalent strain of the outgoing profile of the transport unit."""


Transport.OutProfile.plugin_manager.add_hookspecs(sys.modules[__name__])
