from ..roll_pass import RollPass


@RollPass.Roll.hookspec
def roll_torque(roll_pass: RollPass, roll: RollPass.Roll) -> float:
    """Roll torque of the pass."""


@RollPass.Roll.hookspec
def contact_length(roll_pass: RollPass, roll: RollPass.Roll) -> float:
    """Contact length in rolling direction between rolls and workpiece."""


@RollPass.Roll.hookspec
def contact_area(roll_pass: RollPass, roll: RollPass.Roll) -> float:
    """Area of contact between workpiece and one roll."""
