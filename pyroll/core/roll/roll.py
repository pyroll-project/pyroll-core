import logging
from typing import Iterable, Union

import numpy as np
from shapely.geometry import LineString

from ..grooves import GrooveBase
from ..hooks import HookHost, Hook


class Roll(HookHost):
    """Represents a roll."""

    nominal_radius = Hook[float]()
    """Nominal radius."""

    working_radius = Hook[float]()
    """Effective working radius (equivalent flat rolling)."""

    min_radius = Hook[float]()
    """Minimum radius (at lowest point of groove)."""

    max_radius = Hook[float]()
    """Maximum radius (at highest point of groove)."""

    rotational_frequency = Hook[float]()
    """Rotational frequency (revolutions per time)."""

    surface_velocity = Hook[float]()
    """Tangential velocity of the outer roll surface (at nominal radius)."""

    contour_line = Hook[LineString]()
    """Contour line in the z-y-plane."""

    roll_torque = Hook[float]()
    """Roll torque of single roll."""

    roll_power = Hook[float]()
    """Roll power of single roll."""

    contact_length = Hook[float]()
    """Length of the longest contact arc between roll and workpiece."""

    contact_area = Hook[float]()
    """Total area of contact between roll and workpiece."""

    center = Hook[np.ndarray]()
    """Center point of the roll as 1D array."""

    temperature = Hook[float]()
    """Mean temperature."""

    yield_strength = Hook[float]()
    """Yield strength of the roll material."""

    elastic_modulus = Hook[float]()
    """Elastic modulus of the roll material."""

    poissons_ratio = Hook[float]()
    """Poisson's ratio of the roll material."""

    thermal_conductivity = Hook[float]()
    """Thermal conductivity of the roll material."""

    thermal_capacity = Hook[float]()
    """Thermal capacity of the roll material."""

    density = Hook[float]()
    """Density (specific weight) of the roll material."""

    material = Hook[Union[str, Iterable[str]]]()
    """String or sequence of strings classifying the material of the roll.
    Can be used by material databases to retrieve respective data."""

    def __init__(
            self,
            groove: GrooveBase,
            **kwargs):
        """
        :param groove: the groove object defining the shape of the roll's surface
        :param kwargs: additional hook values as keyword arguments to set explicitly
        """
        self.__dict__.update(kwargs)

        super().__init__()

        self.groove = groove
        """The groove object defining the shape of the roll's surface."""

        self._log = logging.getLogger(__name__)
