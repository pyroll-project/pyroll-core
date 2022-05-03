from ..roll_pass import RollPass


@RollPass.Profile.hookspec
def flow_stress(roll_pass: RollPass, profile: RollPass.Profile) -> float:
    """Flow stress of workpiece material."""
