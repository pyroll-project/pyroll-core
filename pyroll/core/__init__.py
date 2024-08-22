from . import shapes as _

from .grooves import *
from .transport import Transport, CoolingPipe
from .roll_pass import RollPass, DeformationUnit, ThreeRollPass
from .unit import Unit
from .roll import Roll
from .profile import *
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks
from .disk_elements import DiskElementUnit
from .config import Config, config

VERSION = "2.2.0a0"

root_hooks.extend(
    [
        RollPass.roll_force,
        RollPass.Roll.roll_torque,
        RollPass.elongation_efficiency,
        Unit.power,
        Unit.OutProfile.cross_section,
        Unit.OutProfile.classifiers,
        Unit.OutProfile.strain,
        Unit.OutProfile.length,
        Unit.OutProfile.t,
        RollPass.strain_rate,
        RollPass.OutProfile.filling_ratio,
        RollPass.OutProfile.cross_section_filling_ratio,
        RollPass.OutProfile.filling_error,
        RollPass.OutProfile.cross_section_error,
        RollPass.OutProfile.velocity,
        PassSequence.log_elongation,
    ]
)
