import sys

from ..transport import Transport


@Transport.OutProfile.hookimpl
def strain(transport: Transport):
    """Assume total recrystallization during transport."""
    return 0


Transport.OutProfile.plugin_manager.register(sys.modules[__name__])
