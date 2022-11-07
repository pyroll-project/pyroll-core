import logging

from shapely.geometry import LineString

from ..grooves import GrooveBase
from ..hooks import HookHost, Hook


class Roll(HookHost):
    groove: GrooveBase = Hook()
    nominal_radius = Hook[float]()
    working_radius = Hook[float]()
    min_radius = Hook[float]()
    max_radius = Hook[float]()
    rotational_frequency = Hook[float]()
    contour_line = Hook[LineString]()
    roll_torque = Hook[float]()
    contact_length = Hook[float]()
    contact_area = Hook[float]()

    def __init__(
            self,
            groove: GrooveBase,
            **kwargs):
        self.__dict__.update(kwargs)

        super().__init__()

        self.groove = groove
        self._log = logging.getLogger(__name__)
