from typing import Union, Set, List
import numpy as np


from ..hooks import HookHost, Hook

__all__ = ["Engine"]


class Engine(HookHost):
    """Represents an engine of a roll pass."""

    rotational_frequency = Hook[float]()
    """Rotational frequency (revolutions per time)."""

    torque = Hook[float]()
    """Engine torque."""

    idle_torque = Hook[float]()
    """Engine torque in idle state"""

    power = Hook[float]()
    """Power of the engine."""

    gear_ratio = Hook[float]()
    """Gear ratio of the engines gear box."""

    spindle_efficiency = Hook[float]()
    """Efficiency of the spindle that drives the rolls."""

    gear_box_efficiency = Hook[float]()
    """Efficiency of the gear box that drives the rolls."""


    def __init__(self, **kwargs):
        """
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """
        self.__dict__.update(kwargs)

        super().__init__()

    def reevaluate_cache(self):
        super().reevaluate_cache()
