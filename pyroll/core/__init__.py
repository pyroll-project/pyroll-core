VERSION = "2.0.0a3-2"

from . import shapes as _

from .grooves import BoxGroove, ConstrictedBoxGroove, SquareGroove, DiamondGroove, RoundGroove, FalseRoundGroove, \
    CircularOvalGroove, FlatOvalGroove, SwedishOvalGroove, ConstrictedSwedishOvalGroove, Oval3RadiiGroove, \
    Oval3RadiiFlankedGroove, SplineGroove, GenericElongationGroove, FlatGroove
from .transport import Transport
from .roll_pass import RollPass
from .unit import Unit
from .roll import Roll
from .profile import Profile
from .rotator import Rotator
from .sequence import PassSequence
from .hooks import Hook, HookHost, HookFunction, root_hooks

root_hooks.update({
    RollPass.roll_force,
    RollPass.Roll.roll_torque,
    Unit.OutProfile.cross_section,
    Unit.OutProfile.strain,
    Unit.OutProfile.length,
    Unit.OutProfile.types,
    PassSequence.total_elongation,
})
