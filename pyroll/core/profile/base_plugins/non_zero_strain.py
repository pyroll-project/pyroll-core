import sys

from ..profile import Profile


@Profile.hookimpl
def non_zero_strain(profile: Profile):
    return profile.strain + 0.01


Profile.plugin_manager.register(sys.modules[__name__])
