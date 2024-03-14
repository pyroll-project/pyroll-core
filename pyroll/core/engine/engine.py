from typing import Union, Set

import numpy as np
from scipy.interpolate import interpn
from shapely.geometry import LineString

from ..hooks import HookHost, Hook


class Engine(HookHost):
    """Represents a engine."""

    torque = Hook[float]()
    """Torque of the engine."""

    static_torque = Hook[float]()
    """Static torque of the engine."""

    dynamic_torque = Hook[float]()
    """Dynamic torque of the engine."""

    frictional_torque = Hook[float]()
    """Frictional torque of the engine."""

    max_engine_torque = Hook[float]()
    """Max. available torque of the engine."""

    torque_threshold = Hook[float]()
    """Threshold of power of the engine."""

    power = Hook[float]()
    """Power output of the engine."""

    power_threshold = Hook[float]()
    """Power threshold of the engine."""

    bearing_friction_loss_coefficient = Hook[float]()
    """Coefficient of friction loss of the engine bearings."""

    def __init__(
            self,

            **kwargs
    ):
        """
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """
        self.__dict__.update(kwargs)

        super().__init__()

    def reevaluate_cache(self):
        super().reevaluate_cache()
        self._contour_line = None
