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
def length(self: Unit):
    if self.has_set_or_cached("duration"):
        return self.velocity * self.duration


@Unit.duration
def duration(self: Unit):
    if self.has_set_or_cached("length"):
        return self.length / self.velocity


@Unit.velocity
def velocity(self: Unit):
    if self.in_profile.has_set_or_cached("velocity"):
        return self.in_profile.velocity


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
