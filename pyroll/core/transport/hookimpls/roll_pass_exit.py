from ..roll_pass_exit import RollPassExit
from ... import RollPass


def check_if_previous_is_roll_pass(self):
    if not isinstance(self.prev, RollPass):
        raise ValueError("Unit can only follow a RollPass unit.")


@RollPassExit.length
def length(self: RollPassExit):
    check_if_previous_is_roll_pass(self)
    return self.prev.exit_point + self.prev.roll.nominal_radius


@RollPassExit.duration
def duration(self: RollPassExit):
    if self.has_set_or_cached("length"):
        return self.length / self.velocity


@RollPassExit.velocity(
    trylast=True  # do not override getting from in_profile
)
def conti_velocity(self: RollPassExit):
    if self.has_set_or_cached("length"):  # probably indicates conti process
        return self.prev.velocity


@RollPassExit.environment_temperature
def environment_temperature(self: RollPassExit):
    return 25 + 273.15


@RollPassExit.cooling_water_temperature
def cooling_water_temperature(self: RollPassExit):
    return 25 + 273.15
