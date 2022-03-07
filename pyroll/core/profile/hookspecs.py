import sys

from .profile import Profile


@Profile.hookspec
def rotated(profile):
    """Take a profile and calculate its maximum height and width after rotation.
    Return a dict with at least a "height" and a "width" key.
    This will be used to update the profile.
    First implementation that does not return None is taken.
    Do NOT modify the profile object yourself, since this could result in undefined behavior."""


@Profile.hookspec
def equivalent_rectangle(profile):
    """Get the dimensions of the equivalent rectangle of the rotated profile."""


@Profile.hookspec
def non_zero_strain(profile):
    """Return a non null strain, to compensate possible model inadequacies"""


Profile.plugin_manager.add_hookspecs(sys.modules[__name__])
