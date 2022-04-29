import sys
from .roll_pass import RollPass


@RollPass.hookspec
def in_profile_rotation(roll_pass):
    """Rotation of the in profile for the specified roll pass."""


@RollPass.hookspec
def gap(roll_pass):
    """Gap between the rolls."""


@RollPass.hookspec
def nominal_roll_radius(roll_pass):
    """Nominal radius of the rolls (equal to the grooves y=0 axis)."""


@RollPass.hookspec
def working_roll_radius(roll_pass):
    """Working radius of the rolls (some kind of equivalent radius to flat rolling)."""


@RollPass.hookspec
def min_roll_radius(roll_pass):
    """Minimal (inner) radius of the rolls."""


@RollPass.hookspec
def max_roll_radius(roll_pass):
    """Maximal (outer) radius of the rolls."""


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
