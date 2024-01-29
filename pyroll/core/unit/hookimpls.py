from ..config import Config
from .unit import Unit


@Unit.iteration_precision
def default_iteration_precision(self: Unit):
    return Config.DEFAULT_ITERATION_PRECISION


@Unit.max_iteration_count
def default_max_iteration_count(self: Unit):
    return Config.DEFAULT_MAX_ITERATION_COUNT


@Unit.volume
def volume(self: Unit):
    return (self.in_profile.cross_section.area + self.out_profile.cross_section.area) / 2 * self.length


@Unit.surface_area
def surface_area(self: Unit):
    return (self.in_profile.cross_section.perimeter + self.out_profile.cross_section.perimeter) / 2 * self.length


@Unit.length
def length(self: Unit, cycle):
    if not cycle and self.has_value("duration"):
        return self.velocity * self.duration


@Unit.duration
def duration(self: Unit, cycle):
    if not cycle and self.has_value("length"):
        return self.length / self.velocity


@Unit.velocity
def velocity(self: Unit):
    if self.in_profile.has_value("velocity"):
        return self.in_profile.velocity


@Unit.InProfile.length(trylast=True)
def default_in_length(self: Unit.InProfile):
    return 0


@Unit.InProfile.strain(trylast=True)
def default_in_strain(self: Unit.InProfile):
    return 0


@Unit.OutProfile.velocity
def out_velocity(self: Unit.OutProfile):
    if self.unit.in_profile.has_set_or_cached("velocity"):
        return self.unit.in_profile.velocity * self.unit.in_profile.cross_section.area / self.cross_section.area


@Unit.OutProfile.x
def out_x(self: Unit.OutProfile):
    return self.unit.in_profile.x + self.unit.length


@Unit.OutProfile.t
def out_t(self: Unit.OutProfile):
    return self.unit.in_profile.t + self.unit.duration


@Unit.power(trylast=True)
def default_power(self: Unit):
    return 0


@Unit.volume_flux
def volume_flux(self: Unit):
    v = self.out_profile.velocity if self.out_profile.has_value("velocity") else self.velocity
    return self.out_profile.cross_section.area * v


@Unit.mass_flux
def mass_flux(self: Unit):
    return self.volume_flux * self.out_profile.density


@Unit.energy_consumption
def energy_consumption(self: Unit):
    return self.power / self.mass_flux
