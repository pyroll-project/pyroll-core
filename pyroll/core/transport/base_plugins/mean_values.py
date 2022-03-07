import sys

from ..transport import Transport


@Transport.hookimpl
def mean_temperature(transport: Transport):
    return (transport.in_profile.temperature + transport.out_profile.temperature) / 2


Transport.plugin_manager.register(sys.modules[__name__])
