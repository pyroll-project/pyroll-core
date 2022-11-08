import logging

import numpy as np
from shapely.geometry import LineString

from ..grooves import GrooveBase
from ..hooks import HookHost, Hook


class Roll(HookHost):
    groove: GrooveBase = Hook()

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

    def __init__(
            self,
            groove: GrooveBase,
            **kwargs):
        self.__dict__.update(kwargs)

        super().__init__()

        self.groove = groove
        self._log = logging.getLogger(__name__)
