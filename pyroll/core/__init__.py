from . import shapes as _

from .grooves import *
from .transport import Transport, CoolingPipe
from .roll_pass import BaseRollPass, DeformationUnit, ThreeRollPass, SymmetricRollPass, TwoRollPass
from .roll_pass import TwoRollPass as RollPass
from .unit import Unit
from .roll import Roll
from .profile import *
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks
from .disk_elements import DiskElementUnit
from .config import Config, config, PlottingBackend

VERSION = "3.0.1"

root_hooks.extend(
    [
        BaseRollPass.roll_force,
        BaseRollPass.Roll.roll_torque,
        BaseRollPass.elongation_efficiency,
        Unit.power,
        Unit.OutProfile.cross_section,
        Unit.OutProfile.classifiers,
        Unit.OutProfile.strain,
        Unit.OutProfile.length,
        Unit.OutProfile.t,
        BaseRollPass.strain_rate,
        BaseRollPass.OutProfile.filling_ratio,
        BaseRollPass.OutProfile.cross_section_filling_ratio,
        BaseRollPass.OutProfile.filling_error,
        BaseRollPass.OutProfile.cross_section_error,
        BaseRollPass.OutProfile.velocity,
        BaseRollPass.InProfile.velocity,
        PassSequence.log_elongation,
        BaseRollPass.OutProfile.technologically_orientated_cross_section,
        BaseRollPass.technologically_orientated_contour_lines,
    ]
)
