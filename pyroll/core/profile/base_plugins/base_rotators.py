import logging
import sys

import numpy as np

from ..profile import Profile
from ...dimensions import Dimensions


@Profile.hookimpl(specname="rotated", trylast=True)
def error(profile: Profile):
    raise RuntimeError(f"Was not able to rotate the profile shaped by {profile.groove} by {profile.rotation}°.")


@Profile.hookimpl(specname="rotated")
def default(profile: Profile):
    if profile.rotation == 0:
        return Dimensions(profile.width, profile.height)

    if profile.rotation == 90:
        return Dimensions(profile.height, profile.width)

    return None


@Profile.hookimpl(specname="rotated")
def square45(profile: Profile):
    from ...grooves import SquareGroove

    if isinstance(profile.groove, SquareGroove) and profile.rotation == 45:
        d = profile.height + 2 * (profile.groove.r2 / np.cos(profile.groove.alpha2) - profile.groove.r2)
        a = d / np.sqrt(2)

        return Dimensions(a, a)

    return None


@Profile.hookimpl(specname="rotated")
def box45(profile: Profile):
    from ...grooves import BoxGrooveBase

    if isinstance(profile.groove, BoxGrooveBase) and profile.rotation == 45:

        if not np.isclose(profile.height, profile.width, rtol=0.05):
            log = logging.getLogger(__name__)
            log.warning(
                "Box shaped profile significantly deviates from square, rotation by 45° results in asymmetric profile.")

        d = np.sqrt(profile.height ** 2 + profile.width ** 2) - 2 * (np.sqrt(2) - 1) * profile.groove.r2

        return Dimensions(d, d)

    return None


Profile.plugin_manager.register(sys.modules[__name__])
