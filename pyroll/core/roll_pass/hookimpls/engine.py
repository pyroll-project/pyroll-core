import numpy as np

from ..roll_pass import RollPass


@RollPass.Engine.frictional_torque
def frictional_torque(self: RollPass.Engine):
    return self.roll_pass.roll_force * 2 * self.roll_pass.roll.neck_radius * self.bearing_friction_loss_coefficient

@RollPass.Engine.static_torque
def static_torque(self: RollPass.Engine):
    return self.roll_pass.torque