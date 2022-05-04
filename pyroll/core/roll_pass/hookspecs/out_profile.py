from ..roll_pass import RollPass


@RollPass.OutProfile.hookspec
def width(roll_pass: RollPass, profile: RollPass.OutProfile) -> float:
    """Width of the out profile."""


@RollPass.OutProfile.hookspec
def filling_ratio(roll_pass: RollPass, profile: RollPass.OutProfile) -> float:
    """Filling ratio of profile width to usable groove width."""


@RollPass.OutProfile.hookspec
def strain(roll_pass: RollPass, profile: RollPass.OutProfile) -> float:
    """Strain of the out profile."""
