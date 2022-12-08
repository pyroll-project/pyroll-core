from ...pluggy import plugin_manager

from . import units

plugin_manager.register(units)

from . import plots

plugin_manager.register(plots)

from . import format

plugin_manager.register(format)

from ..unit_display import properties

plugin_manager.register(properties)
