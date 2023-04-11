from . import shapes as _

from .grooves import *
from .transport import Transport
from .roll_pass import RollPass, DeformationUnit, ThreeRollPass
from .unit import Unit
from .roll import Roll
from .profile import Profile
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks
from .disk_elements import DiskElementUnit
from .config import Config, config

VERSION = "2.0.2"

root_hooks.update(
    {
        RollPass.roll_force,
        RollPass.Roll.roll_torque,
        Unit.OutProfile.cross_section,
        Unit.OutProfile.strain,
        Unit.OutProfile.length,
        Unit.OutProfile.classifiers,
        Unit.OutProfile.t,
        PassSequence.total_elongation,
    }
)
