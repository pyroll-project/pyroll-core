import numpy as np

from .engine import Engine
from ..config import Config


@Engine.torque
def torque(self: Engine):
    return self.static_torque + self.dynamic_torque


@Engine.bearing_friction_loss_coefficient
def bearing_friction_loss_coefficient(self: Engine):
    return 0.002
