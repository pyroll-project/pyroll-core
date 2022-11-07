from ..roll_pass import RollPass


@RollPass.strain_rate
def strain_rate(self: RollPass):
    return self.velocity / self.roll.contact_length * self.strain_change
