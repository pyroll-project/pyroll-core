from ..roll_pass import RollPass


@RollPass.velocity
def velocity(self: RollPass):
    if hasattr(self.roll, "rotational_frequency"):
        return self.roll.working_radius * self.roll.rotational_frequency
