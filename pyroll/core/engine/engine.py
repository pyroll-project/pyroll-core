from typing import Union, Set, List
import numpy as np


from ..hooks import HookHost, Hook

__all__ = ["Engine"]


class Engine(HookHost):
    """Represents an engine of a roll pass."""

    label = Hook[str]()
    """Type of the engine (DC or AC)"""

    rotational_frequency = Hook[float]()
    """Rotational frequency (revolutions per time)."""

    base_rotational_frequency = Hook[float]()
    """Knee point were a DC engine switches from anchor range to field weakening range."""

    maximum_rotational_frequency = Hook[float]()
    """Maximum rotational frequency of the engine."""

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

    maximum_power = Hook[float]()
    """Maximum power of the engine."""

    available_power = Hook[float]()
    """Available power of the engine only relevant for DC engines."""

    mean_power = Hook[float]()
    """Mean power of the engine incorporating roll pass and transport durations."""


    def __init__(self, **kwargs):
        """
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """
        self.__dict__.update(kwargs)

        super().__init__()

    def reevaluate_cache(self):
        super().reevaluate_cache()
