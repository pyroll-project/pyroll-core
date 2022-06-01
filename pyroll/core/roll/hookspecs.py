from shapely.geometry import LineString

from .roll import Roll
from ..grooves import GrooveBase


@Roll.hookspec
def groove(roll: Roll) -> GrooveBase:
    """Object representing the groove shape carved into the roll."""


@Roll.hookspec
def nominal_radius(roll: Roll) -> float:
    """Nominal radius of the roll (equal to the grooves y=0 axis)."""


@Roll.hookspec
def working_radius(roll: Roll) -> float:
    """Working radius of the roll (some kind of equivalent radius to flat rolling)."""


@Roll.hookspec
def min_radius(roll: Roll) -> float:
    """Minimal (inner) radius of the roll."""


@Roll.hookspec
def max_radius(roll: Roll) -> float:
    """Maximal (outer) radius of the roll."""


@Roll.hookspec
def rotational_frequency(roll: Roll) -> float:
    """The rotational frequency of the roll."""


@Roll.hookspec
def contour_line(roll: Roll) -> LineString:
    """Contour line of the roll's surface."""
