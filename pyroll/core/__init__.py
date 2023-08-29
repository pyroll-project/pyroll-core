from . import shapes as _

from .grooves import *
from .transport import Transport
from .roll_pass import RollPass, DeformationUnit, ThreeRollPass
from .unit import Unit
from .roll import Roll
from .profile import *
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks
from .disk_elements import DiskElementUnit
from .config import Config, config

VERSION = "2.1.0"

root_hooks.update(
    {
        RollPass.roll_force,
        RollPass.Roll.roll_torque,
        RollPass.elongation_efficiency,
        RollPass.OutProfile.filling_ratio,
        RollPass.OutProfile.cross_section_filling_ratio,
        RollPass.OutProfile.filling_error,
        RollPass.OutProfile.cross_section_error,
        Unit.OutProfile.cross_section,
        Unit.OutProfile.strain,
        Unit.OutProfile.length,
        Unit.OutProfile.classifiers,
        Unit.OutProfile.t,
        PassSequence.log_elongation,
        Unit.power,
    }
)
