from ..roll_pass import RollPass

from . import roll_pass

RollPass.plugin_manager.add_hookspecs(roll_pass)

from . import roll

RollPass.Roll.plugin_manager.add_hookspecs(roll)

from . import profile

RollPass.Profile.plugin_manager.add_hookspecs(profile)

from . import out_profile

RollPass.OutProfile.plugin_manager.add_hookspecs(out_profile)
