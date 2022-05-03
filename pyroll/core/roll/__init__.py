from .roll import Roll

from . import hookspecs

Roll.plugin_manager.add_hookspecs(hookspecs)

from . import hookimpls

Roll.plugin_manager.register(hookimpls)

pass