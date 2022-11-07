from ..roll_pass import RollPass


@RollPass.mean_flow_stress
def mean_flow_stress(self: RollPass):
    return (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3


@RollPass.roll_force
def roll_force(self: RollPass):
    return self.mean_flow_stress * self.roll.contact_area


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * 0.5
