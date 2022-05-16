import sys
from typing import List

from pyroll.core import RollPass, Profile, Unit
from pyroll.utils import for_units
from ..reporter import Reporter


def profile_props(prefix, profile: Profile):
    return {
        prefix + "height": "{:.4g}".format(profile.height),
        prefix + "width": "{:.4g}".format(profile.width),
        prefix + "strain": "{:.4g}".format(profile.strain),
        prefix + "temperature": "{:.4g}".format(profile.temperature),
        prefix + "cross section": "{:.4g}".format(profile.cross_section.area),
        prefix + "flow stress": "{:.4g}".format(profile.flow_stress),
    }


@Reporter.hookimpl
@for_units(RollPass)
def unit_properties(unit: RollPass):
    d = {
        "roll force": "{:.4g}".format(unit.roll_force),
        "roll torque": "{:.4g}".format(unit.roll.roll_torque),
        "strain change": "{:.4g}".format(unit.strain_change),
        "spread": "{:.4g}".format(unit.spread),
        "filling ratio": "{:.3f}".format(unit.out_profile.filling_ratio),
        "strain rate": "{:.4g}".format(unit.strain_rate),
        "contact area": "{:.4g}".format(unit.roll.contact_area),
        "contact length": "{:.4g}".format(unit.roll.contact_length),
    }
    d.update(profile_props("in ", unit.in_profile))
    d.update(profile_props("out ", unit.out_profile))
    return d


@Reporter.hookimpl
def sequence_properties(units: List[Unit]):
    return {
        "total elongation": "{:.4g}".format(units[0].in_profile.cross_section.area / units[-1].out_profile.cross_section.area)
    }


Reporter.plugin_manager.register(sys.modules[__name__])
