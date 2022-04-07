import sys

from .transport import TransportOutProfile


@TransportOutProfile.hookspec
def strain(transport):
    """The equivalent strain of the outgoing profile of the transport unit."""


TransportOutProfile.plugin_manager.add_hookspecs(sys.modules[__name__])
