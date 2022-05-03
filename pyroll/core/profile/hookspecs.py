import sys

from .profile import Profile
from ..dimensions import Dimensions


@Profile.hookspec
def rotated(profile: Profile) -> Dimensions:
    """Get the dimensions of the profile rotated by its ``rotation``."""


@Profile.hookspec
def equivalent_rectangle(profile: Profile) -> Dimensions:
    """Get the dimensions of the equivalent rectangle of the rotated profile."""


@Profile.hookspec
def strain(profile: Profile) -> float:
    """Equivalent strain of the profile."""


@Profile.hookspec
def temperature(profile: Profile) -> float:
    """Temperature of the profile."""


@Profile.hookspec
def material(profile: Profile) -> str:
    """Material identifier string for use in several other hooks to get material properties."""


@Profile.hookspec
def flow_stress(profile: Profile) -> str:
    """Flow stress of workpiece material."""


Profile.plugin_manager.add_hookspecs(sys.modules[__name__])
