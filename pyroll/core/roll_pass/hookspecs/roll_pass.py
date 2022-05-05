from ..roll_pass import RollPass


@RollPass.hookspec
def in_profile_rotation(roll_pass: RollPass) -> float:
    """Rotation of the in profile for the specified roll pass."""


@RollPass.hookspec
def gap(roll_pass: RollPass) -> float:
    """Gap between the rolls."""


@RollPass.hookspec
def velocity(roll_pass: RollPass) -> float:
    """Mean rolling velocity."""


@RollPass.hookspec
def height(roll_pass: RollPass) -> float:
    """Maximum height of the pass contour."""


@RollPass.hookspec
def tip_width(roll_pass: RollPass) -> float:
    """Tip width of the pass contour."""


@RollPass.hookspec
def roll_force(roll_pass: RollPass) -> float:
    """Roll force of the pass."""


@RollPass.hookspec
def strain_rate(roll_pass: RollPass) -> float:
    """Mean strain rate in the pass."""


@RollPass.hookspec
def spread(roll_pass: RollPass) -> float:
    """Spread in the pass as ratio b1/b0."""


@RollPass.hookspec
def strain_change(roll_pass: RollPass) -> float:
    """Applied strain in the pass."""