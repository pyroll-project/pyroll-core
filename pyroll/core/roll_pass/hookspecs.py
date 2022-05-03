import sys
from .roll_pass import RollPass


@RollPass.hookspec
def in_profile_rotation(roll_pass):
    """Rotation of the in profile for the specified roll pass."""


@RollPass.hookspec
def gap(roll_pass):
    """Gap between the rolls."""


@RollPass.hookspec
def velocity(roll_pass):
    """Mean rolling velocity."""


@RollPass.hookspec
def height(roll_pass):
    """Maximum height of the pass contour."""


@RollPass.hookspec
def tip_width(roll_pass):
    """Tip width of the pass contour."""


@RollPass.hookspec
def roll_force(roll_pass):
    """Roll force of the pass."""


@RollPass.Roll.hookspec
def roll_torque(roll_pass, roll):
    """Roll torque of the pass."""


@RollPass.hookspec
def strain_rate(roll_pass):
    """Mean strain rate in the pass."""


@RollPass.Roll.hookspec
def contact_length(roll_pass, roll):
    """Contact length in rolling direction between rolls and workpiece."""


@RollPass.Roll.hookspec
def contact_area(roll_pass, roll):
    """Area of contact between workpiece and one roll."""


@RollPass.hookspec
def spread(roll_pass):
    """Spread in the pass as ratio b1/b0."""


@RollPass.hookspec
def strain_change(roll_pass):
    """Applied strain in the pass."""


@RollPass.Profile.hookspec
def flow_stress(roll_pass, profile):
    """Flow stress of workpiece material."""


@RollPass.OutProfile.hookspec
def width(roll_pass, profile):
    """Width of the out profile."""


@RollPass.OutProfile.hookspec
def strain(roll_pass, profile):
    """Strain of the out profile."""


RollPass.plugin_manager.add_hookspecs(sys.modules[__name__])
RollPass.Profile.plugin_manager.add_hookspecs(sys.modules[__name__])
RollPass.OutProfile.plugin_manager.add_hookspecs(sys.modules[__name__])
RollPass.Roll.plugin_manager.add_hookspecs(sys.modules[__name__])
