from ..roll_pass import RollPass


@RollPass.OutProfile.hookspec
def width(roll_pass: RollPass, profile: RollPass.OutProfile) -> float:
    """Width of the out profile."""


@RollPass.OutProfile.hookspec
def strain(roll_pass: RollPass, profile: RollPass.OutProfile) -> float:
    """Strain of the out profile."""
