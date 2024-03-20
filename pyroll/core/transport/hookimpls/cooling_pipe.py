import numpy as np
from ..cooling_pipe import CoolingPipe


@CoolingPipe.inner_radius
def inner_radius(self: CoolingPipe):
    if self.has_set_or_cached("cross_section_area"):
        return np.sqrt(self.cross_section_area / np.pi)


@CoolingPipe.cross_section_area
def cross_section_area(self: CoolingPipe):
    if self.has_set_or_cached("inner_radius"):
        return self.inner_radius ** 2 * np.pi


@CoolingPipe.coolant_flow_cross_section
def coolant_flow_cross_section(self: CoolingPipe):
    return self.cross_section_area - self.in_profile.cross_section.area


@CoolingPipe.coolant_velocity
def coolant_velocity(self: CoolingPipe):
    return self.coolant_volume_flux / self.coolant_flow_cross_section
