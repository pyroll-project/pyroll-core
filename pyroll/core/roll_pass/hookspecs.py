import sys
from .roll_pass import RollPass, RollPassOutProfile, RollPassProfile


@RollPass.hookspec
def in_profile_rotation(roll_pass):
    """Rotation of the in profile for the specified roll pass."""


@RollPass.hookspec
def roll_force(roll_pass):
    """Roll force of the pass."""


@RollPass.hookspec
def roll_torque(roll_pass):
    """Roll torque of the pass."""


@RollPass.hookspec
def strain_rate(roll_pass):
    """Mean strain rate in the pass."""


@RollPass.hookspec
def contact_length(roll_pass):
    """Contact length in rolling direction between rolls and workpiece."""


@RollPass.hookspec
def contact_area(roll_pass):
    """Area of contact between workpiece and one roll."""


@RollPass.hookspec
def width_change(roll_pass):
    """Spread in the pass as width difference."""


@RollPass.hookspec
def strain_change(roll_pass):
    """Applied strain in the pass."""


@RollPass.hookspec
def mean_temperature(roll_pass):
    """Mean temperature of workpiece in the pass."""


@RollPass.hookspec
def mean_flow_stress(roll_pass):
    """Mean flow stress of workpiece in the pass."""


@RollPassProfile.hookspec
def flow_stress(roll_pass, profile):
    """Flow stress of workpiece material."""


@RollPassOutProfile.hookspec
def width(roll_pass, profile):
    """Width of the out profile."""


@RollPassOutProfile.hookspec
def strain(roll_pass, profile):
    """Strain of the out profile."""


RollPass.plugin_manager.add_hookspecs(sys.modules[__name__])
RollPassProfile.plugin_manager.add_hookspecs(sys.modules[__name__])
RollPassOutProfile.plugin_manager.add_hookspecs(sys.modules[__name__])
