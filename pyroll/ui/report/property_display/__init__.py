from ...pluggy import plugin_manager

from . import format

plugin_manager.register(format)

from . import properties

plugin_manager.register(properties)