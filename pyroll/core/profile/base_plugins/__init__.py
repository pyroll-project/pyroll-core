from ..profile import Profile

from . import equivalent_rectangle

Profile.plugin_manager.register(equivalent_rectangle)

from . import shape

Profile.plugin_manager.register(shape)
