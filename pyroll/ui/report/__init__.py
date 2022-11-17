from .report import report
from ..pluggy import plugin_manager

from . import hookspecs

plugin_manager.add_hookspecs(hookspecs)

from . import property_display

plugin_manager.register(property_display)
