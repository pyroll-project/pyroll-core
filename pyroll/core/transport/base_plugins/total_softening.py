import sys

from ..transport import TransportOutProfile, Transport


@TransportOutProfile.hookimpl
def strain(transport: Transport):
    """Assume total recrystallization during transport."""
    return 0


TransportOutProfile.hooks.add("strain")

TransportOutProfile.plugin_manager.register(sys.modules[__name__])
