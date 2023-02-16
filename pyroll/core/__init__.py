VERSION = "2.0.0rc1"

from . import shapes as _

from .grooves import (
    BoxGroove, ConstrictedBoxGroove, UpsetBoxGroove, ConstrictedUpsetBoxGroove,
    SquareGroove, DiamondGroove, GothicGroove,
    RoundGroove, FalseRoundGroove,
    CircularOvalGroove, FlatOvalGroove, SwedishOvalGroove, ConstrictedSwedishOvalGroove, Oval3RadiiGroove,
    Oval3RadiiFlankedGroove, UpsetOvalGroove,
    SplineGroove,
    GenericElongationGroove,
    FlatGroove,
    HexagonalGroove
)
from .transport import Transport
from .roll_pass import RollPass, DeformationUnit, ThreeRollPass
from .unit import Unit
from .roll import Roll
from .profile import Profile
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks
from .disk_elements import DiskElementUnit

root_hooks.update(
    {
        RollPass.roll_force,
        RollPass.Roll.roll_torque,
        Unit.OutProfile.cross_section,
        Unit.OutProfile.strain,
        Unit.OutProfile.length,
        Unit.OutProfile.types,
        Unit.OutProfile.t,
        PassSequence.total_elongation,
    }
)
