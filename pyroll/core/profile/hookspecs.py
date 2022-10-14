import sys
from typing import Iterable, Union

from shapely.geometry import Polygon, LineString

from .profile import Profile


@Profile.hookspec
def upper_contour_line(profile: Profile) -> LineString:
    """Upper bounding contour line of the profile."""


@Profile.hookspec
def lower_contour_line(profile: Profile) -> LineString:
    """Lower bounding contour line of the profile."""


@Profile.hookspec
def cross_section(profile: Profile) -> Polygon:
    """Cross-section polygon of the profile."""


@Profile.hookspec
def height(profile: Profile) -> float:
    """Height of the profile."""


@Profile.hookspec
def width(profile: Profile) -> float:
    """Width of the profile."""


@Profile.hookspec
def types(profile: Profile) -> float:
    """A tuple of keywords to specify the shape types of the profile."""


@Profile.hookspec
def equivalent_rectangle(profile: Profile) -> Polygon:
    """Get the dimensions of the equivalent rectangle of the profile."""


@Profile.hookspec
def strain(profile: Profile) -> float:
    """Equivalent strain of the profile."""


@Profile.hookspec
def temperature(profile: Profile) -> float:
    """Temperature of the profile."""


@Profile.hookspec
def material(profile: Profile) -> Union[str, Iterable[str]]:
    """Material identifier string for use in several other hooks to get material properties."""


@Profile.hookspec
def flow_stress(profile: Profile) -> str:
    """Flow stress of workpiece material."""


Profile.plugin_manager.add_hookspecs(sys.modules[__name__])
